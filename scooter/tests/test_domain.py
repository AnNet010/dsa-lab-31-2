import pytest
from datetime import datetime

from scooter.domain.value_objects import Battery, Money, TripPeriod
from scooter.domain.scooter import Scooter
from scooter.domain.trip import Trip
from scooter.domain.services import StartTripService
from scooter.domain.exceptions import DomainInvariantViolation, InvalidValueObject
from scooter.infrastructure.in_memory import InMemoryScooterRepository, InMemoryTripRepository


def test_scooter_low_battery():
    scooter = Scooter(1, Battery(10), status="free")
    with pytest.raises(DomainInvariantViolation):
        scooter.start_trip()


def test_trip_cannot_be_finished_twice():
    period = TripPeriod(datetime(2026, 1, 1), datetime(2026, 1, 1, 0, 30))
    trip = Trip(1, 1, 1, period)
    trip.finish(datetime(2026, 1, 1, 0, 30), Money(100), Money(50))
    with pytest.raises(DomainInvariantViolation):
        trip.finish(datetime(2026, 1, 1, 0, 40), Money(150), Money(50))


def test_start_trip_service():
    scooter_repo = InMemoryScooterRepository()
    trip_repo = InMemoryTripRepository()

    scooter = Scooter(1, Battery(80))
    scooter_repo.save(scooter)

    service = StartTripService(scooter_repo, trip_repo)
    period = TripPeriod(datetime(2026, 1, 1), datetime(2026, 1, 1, 0, 30))
    trip = service.start_trip(1, 1, 1, period)

    assert scooter.status == "in_use"
    assert trip_repo.get(1) is not None