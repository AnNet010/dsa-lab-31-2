from dataclasses import dataclass
from datetime import datetime
from .exceptions import InvalidValueObject


@dataclass(frozen=True)
class SpotNumber:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 1:
            raise InvalidValueObject("Номер места не может быть пустым")


@dataclass(frozen=True)
class Money:
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidValueObject("Сумма не может быть отрицательной")


@dataclass(frozen=True)
class ParkingPeriod:
    entry_time: datetime
    exit_time: datetime

    def __post_init__(self):
        if self.exit_time < self.entry_time:
            raise InvalidValueObject(
                "Время выезда не может быть раньше времени въезда"
            )

    def hours(self) -> int:
        delta = self.exit_time - self.entry_time
        seconds = delta.total_seconds()
        return max(1, -(-int(seconds) // 3600))


@dataclass(frozen=True)
class CarNumber:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 4:
            raise InvalidValueObject("Номер машины слишком короткий")