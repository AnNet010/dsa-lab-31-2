from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from .exceptions import DomainInvariantViolation
from .value_objects import TripPeriod, Money
from .trip_states import (
    TripState, Reserved, Active, Paused, Finished,
    RejectedInZone, Cancelled, NotStarted,
)
from .events import (
    TripReserved, TripReservationExpired, TripRejected,
    TripStarted, TripPaused, TripResumed, TripFinished,
    TripRejectedInZone, LongTripNotification,
)


class Trip:
    def __init__(self, trip_id: int, scooter_id: int, user_id: int,
                 period: TripPeriod):
        self._id = trip_id
        self._scooter_id = scooter_id
        self._user_id = user_id
        self._period = period
        self._cost: Optional[Money] = None
        self._state: TripState = Reserved()
        self._events: List = []
        self._is_in_allowed_zone = False
        self._photo_attached = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def scooter_id(self) -> int:
        return self._scooter_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def status(self) -> str:
        return self._state.name

    @property
    def allowed_events(self) -> frozenset[str]:
        return self._state.allowed

    @property
    def events(self) -> tuple:
        return tuple(self._events)

    @property
    def cost(self) -> Optional[Money]:
        return self._cost

    @property
    def is_in_allowed_zone(self) -> bool:
        return self._is_in_allowed_zone

    def pay_authorized(self, now: datetime) -> None:
        self._state = self._state.pay_authorized(self)
        self._events.append(TripStarted(self._id, now))

    def pay_failed(self, now: datetime, reason: str = "Авторизация не прошла") -> None:
        self._state = self._state.pay_failed(self)
        self._events.append(TripRejected(self._id, reason, now))

    def expire(self, now: datetime) -> None:
        self._state = self._state.expire(self)
        self._events.append(TripReservationExpired(self._id, now))

    def pause(self, now: datetime) -> None:
        self._state = self._state.pause(self)
        self._events.append(TripPaused(self._id, now))

    def resume(self, now: datetime) -> None:
        self._state = self._state.resume(self)
        self._events.append(TripResumed(self._id, now))

    def finish(self, now: datetime, cost: Money, min_cost: Money) -> None:
        if cost.amount < min_cost.amount:
            raise DomainInvariantViolation(
                "Стоимость не может быть меньше минимальной"
            )
        self._state = self._state.finish(self)
        self._cost = cost
        self._events.append(TripFinished(self._id, cost.amount, now))

    def reject_zone(self, now: datetime) -> None:
        self._state = self._state.reject_zone(self)
        self._events.append(TripRejectedInZone(self._id, now))

    def mark_in_zone(self) -> None:
        self._is_in_allowed_zone = True

    def attach_photo(self) -> None:
        self._photo_attached = True

    def is_long_trip(self, now: datetime) -> bool:
        return self._period.duration_hours() > 12

    def on_long_trip(self, now: datetime) -> None:
        self._events.append(LongTripNotification(self._id, now))

    @classmethod
    def restore(cls, trip_id: int, scooter_id: int, user_id: int,
                period: TripPeriod, cost: Optional[Money] = None,
                state_name: str = "Забронирована",
                is_in_allowed_zone: bool = False) -> "Trip":
        trip = cls(trip_id, scooter_id, user_id, period)
        trip._cost = cost
        trip._is_in_allowed_zone = is_in_allowed_zone
        mapping = {
            "Забронирована": Reserved,
            "Активна": Active,
            "На паузе": Paused,
            "Завершена": Finished,
            "Отклонена": RejectedInZone,
            "Отменена": Cancelled,
            "Не начата": NotStarted,
        }
        state_cls = mapping.get(state_name)
        if state_cls is None:
            raise DomainInvariantViolation(f"Неизвестное состояние: {state_name}")
        trip._state = state_cls()
        return trip