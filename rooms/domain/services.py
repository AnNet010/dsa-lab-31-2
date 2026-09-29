from datetime import datetime
from .room import Room
from .booking import Booking
from .value_objects import TimeSlot, Participants
from .exceptions import DomainInvariantViolation


class BookingService:
    def __init__(self, room_repo, booking_repo):
        self._room_repo = room_repo
        self._booking_repo = booking_repo

    def book(self, booking_id: int, room_id: int, employee_id: int,
             slot: TimeSlot, participants: Participants) -> Booking:
        room = self._room_repo.get(room_id)
        if room is None:
            raise DomainInvariantViolation("Комната не найдена")

        if not room.can_fit(participants.value):
            raise DomainInvariantViolation(
                "Число участников превышает вместимость комнаты"
            )

        if slot.start_time.time() < room.office_hours.start:
            raise DomainInvariantViolation(
                "Бронь не может начинаться раньше начала работы офиса"
            )
        if slot.end_time.time() > room.office_hours.end:
            raise DomainInvariantViolation(
                "Бронь не может заканчиваться позже конца работы офиса"
            )

        for existing in self._booking_repo.list_by_room(room_id):
            if existing.slot.overlaps(slot):
                raise DomainInvariantViolation(
                    "Бронь пересекается с существующей"
                )

        booking = Booking(booking_id, room_id, employee_id, slot, participants)
        self._booking_repo.save(booking)
        return booking