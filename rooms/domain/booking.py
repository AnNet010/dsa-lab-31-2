from typing import Optional
from .exceptions import DomainInvariantViolation
from .value_objects import TimeSlot, Participants


class Booking:
    def __init__(self, booking_id: int, room_id: int, employee_id: int,
                 slot: TimeSlot, participants: Participants):
        self._id = booking_id
        self._room_id = room_id
        self._employee_id = employee_id
        self._slot = slot
        self._participants = participants

    @property
    def id(self) -> int:
        return self._id

    @property
    def room_id(self) -> int:
        return self._room_id

    @property
    def employee_id(self) -> int:
        return self._employee_id

    @property
    def slot(self) -> TimeSlot:
        return self._slot

    @property
    def participants(self) -> Participants:
        return self._participants

    def overlaps_with(self, other: "Booking") -> bool:
        if self._room_id != other._room_id:
            return False
        return self._slot.overlaps(other._slot)

    @classmethod
    def restore(cls, booking_id: int, room_id: int, employee_id: int,
                slot: TimeSlot, participants: Participants) -> "Booking":
        return cls(booking_id, room_id, employee_id, slot, participants)