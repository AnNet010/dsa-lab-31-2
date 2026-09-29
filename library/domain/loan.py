from datetime import datetime
from typing import Optional
from library.domain.exceptions import DomainInvariantViolation
from library.domain.value_objects import LoanPeriod, Fine


class Loan:
    def __init__(self, loan_id: int, book_id: int, reader_id: int,
                 period: LoanPeriod):
        self._id = loan_id
        self._book_id = book_id
        self._reader_id = reader_id
        self._period = period
        self._return_date: Optional[datetime] = None
        self._fine: Optional[Fine] = None
        self._is_closed = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def book_id(self) -> int:
        return self._book_id

    @property
    def reader_id(self) -> int:
        return self._reader_id

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    def close(self, return_date: datetime, fine: Optional[Fine] = None):
        if self._is_closed:
            raise DomainInvariantViolation("Выдача уже закрыта")
        if return_date < self._period.start_date:
            raise DomainInvariantViolation(
                "Дата возврата не может быть раньше даты выдачи"
            )
        self._return_date = return_date
        if return_date > self._period.due_date:
            if fine is None:
                raise DomainInvariantViolation(
                    "При просрочке должен быть рассчитан штраф"
                )
            self._fine = fine
        self._is_closed = True

    @classmethod
    def restore(cls, loan_id: int, book_id: int, reader_id: int,
                period: LoanPeriod, return_date: Optional[datetime] = None,
                fine: Optional[Fine] = None,
                is_closed: bool = False) -> "Loan":
        loan = cls(loan_id, book_id, reader_id, period)
        loan._return_date = return_date
        loan._fine = fine
        loan._is_closed = is_closed

        if is_closed and return_date is None:
            raise DomainInvariantViolation(
                "Закрытая выдача должна иметь дату возврата"
            )
        return loan