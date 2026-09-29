import pytest
from datetime import datetime, time

from rooms.domain.value_objects import Capacity, Participants, TimeSlot, OfficeHours
from rooms.domain.room import Room
from rooms.domain.services import BookingService
from rooms.domain.exceptions import DomainInvariantViolation
from rooms.infrastructure.in_memory import InMemoryRoomRepository, InMemoryBookingRepository


def test_room_can_fit():
    room = Room(1, "A1", Capacity(10), OfficeHours(time(9), time(18)))
    assert room.can_fit(5) is True
    assert room.can_fit(15) is False


def test_booking_service_participants_exceed_capacity():
    room_repo = InMemoryRoomRepository()
    booking_repo = InMemoryBookingRepository()

    room = Room(1, "A1", Capacity(5), OfficeHours(time(9), time(18)))
    room_repo.save(room)

    service = BookingService(room_repo, booking_repo)
    slot = TimeSlot(datetime(2026, 1, 1, 10), datetime(2026, 1, 1, 11))

    with pytest.raises(DomainInvariantViolation):
        service.book(1, 1, 1, slot, Participants(10))