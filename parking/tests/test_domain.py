import pytest
from datetime import datetime

from parking.domain.value_objects import SpotNumber, Money
from parking.domain.parking_spot import ParkingSpot
from parking.domain.parking_session import ParkingSession
from parking.domain.services import ParkingService
from parking.domain.exceptions import DomainInvariantViolation
from parking.infrastructure.in_memory import (
    InMemoryParkingSpotRepository, InMemoryParkingSessionRepository
)


def test_spot_occupy_twice():
    spot = ParkingSpot(1, SpotNumber("A1"))
    spot.occupy()
    with pytest.raises(DomainInvariantViolation):
        spot.occupy()


def test_session_cannot_be_closed_twice():
    session = ParkingSession(1, 1, 1, datetime(2026, 1, 1, 10))
    session.close(datetime(2026, 1, 1, 12), Money(200))
    with pytest.raises(DomainInvariantViolation):
        session.close(datetime(2026, 1, 1, 13), Money(300))


def test_parking_service_enter_and_exit():
    spot_repo = InMemoryParkingSpotRepository()
    session_repo = InMemoryParkingSessionRepository()

    spot = ParkingSpot(1, SpotNumber("A1"))
    spot_repo.save(spot)

    service = ParkingService(spot_repo, session_repo)
    session = service.enter(1, 1, 1, datetime(2026, 1, 1, 10))

    assert spot.status == "occupied"

    service.exit(1, datetime(2026, 1, 1, 12), Money(200))
    assert spot.status == "free"
    assert session.is_closed is True