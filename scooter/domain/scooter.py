from datetime import datetime
from typing import Optional
from .exceptions import DomainInvariantViolation
from .value_objects import Battery, ReservationPeriod


class Scooter:
    MIN_BATTERY = 20

    def __init__(self, scooter_id: int, battery: Battery, status: str = "free"):
        self._id = scooter_id
        self._battery = battery
        self._status = status
        self._reservation: Optional[ReservationPeriod] = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def status(self) -> str:
        return self._status

    @property
    def reservation(self) -> Optional[ReservationPeriod]:
        return self._reservation

    def can_be_rented(self) -> bool:
        return (
            self._status == "free"
            and self._battery.level >= self.MIN_BATTERY
        )

    def reserve(self, period: ReservationPeriod) -> None:
        if not self.can_be_rented():
            raise DomainInvariantViolation(
                "Самокат не может быть забронирован, низкий заряд или занят"
            )
        self._status = "reserved"
        self._reservation = period

    def cancel_reservation(self) -> None:
        if self._status != "reserved":
            raise DomainInvariantViolation("Самокат не забронирован")
        self._status = "free"
        self._reservation = None

    def unlock(self) -> None:
        if self._status != "reserved":
            raise DomainInvariantViolation(
                "Нельзя разблокировать, самокат не забронирован"
            )
        self._status = "in_use"
        self._reservation = None

    def finish_trip(self) -> None:
        if self._status != "in_use":
            raise DomainInvariantViolation("Самокат не в поездке")
        self._status = "free"

    @classmethod
    def restore(cls, scooter_id: int, battery: Battery,
                status: str, reservation: Optional[ReservationPeriod] = None) -> "Scooter":
        scooter = cls(scooter_id, battery, status)
        scooter._reservation = reservation
        if status not in ("free", "reserved", "in_use", "maintenance"):
            raise DomainInvariantViolation("Некорректный статус самоката")
        return scooter