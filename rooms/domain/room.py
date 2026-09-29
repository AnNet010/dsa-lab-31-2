from .exceptions import DomainInvariantViolation
from .value_objects import Capacity, OfficeHours


class Room:
    def __init__(self, room_id: int, name: str, capacity: Capacity,
                 office_hours: OfficeHours):
        self._id = room_id
        self._name = name
        self._capacity = capacity
        self._office_hours = office_hours

    @property
    def id(self) -> int:
        return self._id

    @property
    def capacity(self) -> Capacity:
        return self._capacity

    @property
    def office_hours(self) -> OfficeHours:
        return self._office_hours

    def can_fit(self, participants: int) -> bool:
        return participants <= self._capacity.value

    @classmethod
    def restore(cls, room_id: int, name: str, capacity: Capacity,
                office_hours: OfficeHours) -> "Room":
        return cls(room_id, name, capacity, office_hours)