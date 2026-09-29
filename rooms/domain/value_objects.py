from dataclasses import dataclass
from datetime import datetime, time
from .exceptions import InvalidValueObject


@dataclass(frozen=True)
class Capacity:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidValueObject("Вместимость должна быть > 0")


@dataclass(frozen=True)
class Participants:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidValueObject("Число участников должно быть > 0")


@dataclass(frozen=True)
class TimeSlot:
    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise InvalidValueObject(
                "Время окончания должно быть позже времени начала"
            )

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start_time < other.end_time and other.start_time < self.end_time


@dataclass(frozen=True)
class OfficeHours:
    start: time
    end: time

    def __post_init__(self):
        if self.end <= self.start:
            raise InvalidValueObject("Конец работы должен быть позже начала")