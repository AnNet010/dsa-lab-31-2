from .exceptions import DomainInvariantViolation
from .value_objects import SpotNumber


class ParkingSpot:
    def __init__(self, spot_id: int, number: SpotNumber, status: str = "free"):
        self._id = spot_id
        self._number = number
        self._status = status

    @property
    def id(self) -> int:
        return self._id

    @property
    def number(self) -> SpotNumber:
        return self._number

    @property
    def status(self) -> str:
        return self._status

    def can_be_occupied(self) -> bool:
        return self._status == "free"

    def occupy(self):
        if not self.can_be_occupied():
            raise DomainInvariantViolation("Место уже занято")
        self._status = "occupied"

    def free(self):
        if self._status != "occupied":
            raise DomainInvariantViolation("Место не занято")
        self._status = "free"

    @classmethod
    def restore(cls, spot_id: int, number: SpotNumber, status: str) -> "ParkingSpot":
        spot = cls(spot_id, number, status)
        if status not in ("free", "occupied"):
            raise DomainInvariantViolation("Некорректный статус места")
        return spot