from dataclasses import dataclass
from datetime import datetime
from .exceptions import InvalidValueObject


@dataclass(frozen=True)
class Battery:
    level: int

    def __post_init__(self):
        if self.level < 0 or self.level > 100:
            raise InvalidValueObject("Уровень заряда должен быть от 0 до 100")


@dataclass(frozen=True)
class Money:
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidValueObject("Сумма не может быть отрицательной")


@dataclass(frozen=True)
class TripPeriod:
    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        if self.end_time < self.start_time:
            raise InvalidValueObject("Время окончания не может быть раньше времени начала")


@dataclass(frozen=True)
class UserId:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidValueObject("UserId должен быть > 0")