import pytest
from datetime import datetime, timedelta

from scooter.domain.value_objects import Battery, Money, TripPeriod
from scooter.domain.trip import Trip
from scooter.domain.user import User
from scooter.domain.scooter import Scooter
from scooter.domain.exceptions import TransitionNotAllowed
from scooter.domain.services import ScooterProcess
from scooter.infrastructure.in_memory import (
    InMemoryScooterRepository, InMemoryTripRepository,
    InMemoryUserRepository, InMemoryPaymentGateway,
)
from scooter.infrastructure.clock import ShiftedClock


FUTURE = datetime(2099, 1, 1, 10, 0)


def _make_process():
    scooter_repo = InMemoryScooterRepository()
    trip_repo = InMemoryTripRepository()
    user_repo = InMemoryUserRepository()
    payment = InMemoryPaymentGateway()
    clock = ShiftedClock()
    clock.move_to(FUTURE)

    scooter_repo.save(Scooter(1, Battery(80)))
    user_repo.save(User(1, has_debt=False))

    process = ScooterProcess(scooter_repo, trip_repo, user_repo, payment, clock)
    return process, scooter_repo, trip_repo, user_repo, payment, clock


def test_successful_trip():
    process, scooter_repo, trip_repo, user_repo, payment, clock = _make_process()
    trip = process.reserve_scooter(1, 1, 1, FUTURE)
    process.start_trip(1, 1)

    assert trip.status == "Активна"

    process.finish_trip(1, Money(200), is_in_zone=True)
    assert trip.status == "Завершена"
    assert scooter_repo.get(1).status == "free"


def test_transition_not_allowed():
    period = TripPeriod(FUTURE, FUTURE + timedelta(minutes=30))
    trip = Trip(1, 1, 1, period)

    with pytest.raises(TransitionNotAllowed):
        trip.pause(FUTURE + timedelta(minutes=5))


def test_reservation_expires():
    process, scooter_repo, trip_repo, user_repo, payment, clock = _make_process()
    trip = process.reserve_scooter(1, 1, 1, FUTURE)

    clock.move_to(FUTURE + timedelta(minutes=11))
    process.on_reservation_expired(clock.now())

    assert trip.status == "Отменена"
    assert scooter_repo.get(1).status == "free"