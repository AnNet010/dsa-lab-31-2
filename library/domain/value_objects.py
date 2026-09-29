from dataclasses import dataclass
from datetime import datetime
from library.domain.exceptions import InvalidValueObject


@dataclass(frozen=True)
class ISBN:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 10:
            raise InvalidValueObject("ISBN должен быть не короче 10 символов")


@dataclass(frozen=True)
class ReaderId:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidValueObject("ReaderId должен быть > 0")


@dataclass(frozen=True)
class LoanPeriod:
    start_date: datetime
    due_date: datetime

    def __post_init__(self):
        if self.due_date < self.start_date:
            raise InvalidValueObject("Срок возврата не может быть раньше даты выдачи")


@dataclass(frozen=True)
class Fine:
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidValueObject("Сумма штрафа не может быть отрицательной")