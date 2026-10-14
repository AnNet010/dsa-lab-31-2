from datetime import datetime, timedelta
from .scooter import Scooter
from .trip import Trip
from .user import User
from .value_objects import TripPeriod, Money, ReservationPeriod
from .exceptions import DomainInvariantViolation, GatewayUnresolved
from .clock import Clock
from .ports import PaymentGateway
from .events import TripReserved


RESERVATION_TIMEOUT = timedelta(minutes=10)
MIN_TRIP_COST = Money(50)
AUTH_AMOUNT = 300.0


def is_debt_present(has_debt: bool) -> bool:
    return has_debt


def is_not_debt_present(has_debt: bool) -> bool:
    return not has_debt


def is_payment_authorized(result: bool) -> bool:
    return result


def is_payment_failed(result: bool) -> bool:
    return not result


def is_in_allowed_zone(is_in_zone: bool) -> bool:
    return is_in_zone


def is_out_of_zone(is_in_zone: bool) -> bool:
    return not is_in_zone


def is_payment_charged(result: bool) -> bool:
    return result


def is_payment_not_charged(result: bool) -> bool:
    return not result


class ScooterProcess:
    def __init__(self, scooter_repo, trip_repo, user_repo,
                 payment_gateway: PaymentGateway, clock: Clock):
        self._scooter_repo = scooter_repo
        self._trip_repo = trip_repo
        self._user_repo = user_repo
        self._payment = payment_gateway
        self._clock = clock

    def reserve_scooter(self, trip_id: int, scooter_id: int,
                        user_id: int, start_time: datetime) -> Trip:
        scooter = self._scooter_repo.get(scooter_id)
        if scooter is None:
            raise DomainInvariantViolation("Самокат не найден")

        now = self._clock.now()
        period = ReservationPeriod(until=now + RESERVATION_TIMEOUT)
        scooter.reserve(period)

        trip_period = TripPeriod(start_time, start_time)
        trip = Trip(trip_id, scooter_id, user_id, trip_period)

        trip._events.append(TripReserved(trip_id, now))

        self._scooter_repo.save(scooter)
        self._trip_repo.save(trip)
        return trip

    def check_debt(self, user_id: int) -> bool:
        user = self._user_repo.get(user_id)
        if user is None:
            raise DomainInvariantViolation("Пользователь не найден")
        return user.check_debt()

    def authorize_payment(self) -> bool:
        return self._payment.authorize(AUTH_AMOUNT)

    def start_trip(self, trip_id: int, scooter_id: int) -> Trip:
        scooter = self._scooter_repo.get(scooter_id)
        if scooter is None:
            raise DomainInvariantViolation("Самокат не найден")

        trip = self._trip_repo.get(trip_id)
        if trip is None:
            raise DomainInvariantViolation("Поездка не найдена")

        now = self._clock.now()
        has_debt = self.check_debt(trip.user_id)

        if is_debt_present(has_debt):
            trip.pay_failed(now, reason="Задолженность")
            if scooter.status == "reserved":
                scooter.cancel_reservation()
                self._scooter_repo.save(scooter)
            self._trip_repo.save(trip)
            return trip
        elif is_not_debt_present(has_debt):
            pass
        else:
            raise GatewayUnresolved("Задолженность есть?")

        authorized = self.authorize_payment()

        if is_payment_authorized(authorized):
            pass
        elif is_payment_failed(authorized):
            trip.pay_failed(now, reason="Авторизация не прошла")
            if scooter.status == "reserved":
                scooter.cancel_reservation()
                self._scooter_repo.save(scooter)
            self._trip_repo.save(trip)
            return trip
        else:
            raise GatewayUnresolved("Авторизация прошла?")

        scooter.unlock()
        trip.pay_authorized(now)

        self._scooter_repo.save(scooter)
        self._trip_repo.save(trip)
        return trip

    def pause_trip(self, trip_id: int) -> None:
        trip = self._trip_repo.get(trip_id)
        if trip is None:
            raise DomainInvariantViolation("Поездка не найдена")
        trip.pause(self._clock.now())
        self._trip_repo.save(trip)

    def resume_trip(self, trip_id: int) -> None:
        trip = self._trip_repo.get(trip_id)
        if trip is None:
            raise DomainInvariantViolation("Поездка не найдена")
        trip.resume(self._clock.now())
        self._trip_repo.save(trip)

    def finish_trip(self, trip_id: int, cost: Money,
                    is_in_zone: bool) -> None:
        trip = self._trip_repo.get(trip_id)
        if trip is None:
            raise DomainInvariantViolation("Поездка не найдена")

        now = self._clock.now()

        if is_in_allowed_zone(is_in_zone):
            trip.mark_in_zone()
            trip.finish(now, cost, MIN_TRIP_COST)

            charged = self._payment.charge(trip_id, cost.amount)

            if is_payment_charged(charged):
                pass
            elif is_payment_not_charged(charged):
                user = self._user_repo.get(trip.user_id)
                if user is not None:
                    user.block(now)
                    self._user_repo.save(user)
            else:
                raise GatewayUnresolved("Списание прошло?")

            scooter = self._scooter_repo.get(trip.scooter_id)
            if scooter is not None and scooter.status == "in_use":
                scooter.finish_trip()
                self._scooter_repo.save(scooter)

            self._trip_repo.save(trip)

        elif is_out_of_zone(is_in_zone):
            trip.reject_zone(now)

            scooter = self._scooter_repo.get(trip.scooter_id)
            if scooter is not None and scooter.status == "in_use":
                scooter.finish_trip()
                self._scooter_repo.save(scooter)

            self._trip_repo.save(trip)
        else:
            raise GatewayUnresolved("В зоне?")

    def on_reservation_expired(self, now: datetime) -> None:
        for trip in self._trip_repo.all():
            if "expire" in trip.allowed_events:
                trip.expire(now)
                scooter = self._scooter_repo.get(trip.scooter_id)
                if scooter is not None and scooter.status == "reserved":
                    scooter.cancel_reservation()
                    self._scooter_repo.save(scooter)
                self._trip_repo.save(trip)

    def on_long_trip(self, now: datetime) -> None:
        for trip in self._trip_repo.all():
            if trip.is_long_trip(now):
                trip.on_long_trip(now)
                self._trip_repo.save(trip)