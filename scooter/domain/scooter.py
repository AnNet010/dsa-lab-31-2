from .exceptions import DomainInvariantViolation
from .value_objects import Battery


class Scooter:
    MIN_BATTERY = 20

    def __init__(self, scooter_id: int, battery: Battery, status: str = "free"):
        self._id = scooter_id
        self._battery = battery
        self._status = status

    @property
    def id(self) -> int:
        return self._id

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def status(self) -> str:
        return self._status

    def can_be_rented(self) -> bool:
        return (
            self._status == "free"
            and self._battery.level >= self.MIN_BATTERY
        )

    def start_trip(self):
        if not self.can_be_rented():
            raise DomainInvariantViolation(
                "Самокат не может быть выдан: низкий заряд или занят"
            )
        self._status = "in_use"

    def finish_trip(self):
        if self._status != "in_use":
            raise DomainInvariantViolation("Самокат не в поездке")
        self._status = "free"

    @classmethod
    def restore(cls, scooter_id: int, battery: Battery, status: str) -> "Scooter":
        scooter = cls(scooter_id, battery, status)
        if status not in ("free", "in_use", "maintenance"):
            raise DomainInvariantViolation("Некорректный статус самоката")
        return scooter