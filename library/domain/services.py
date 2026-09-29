from datetime import datetime
from typing import Optional
from library.domain.book import Book
from library.domain.loan import Loan
from library.domain.value_objects import LoanPeriod, Fine
from library.domain.exceptions import DomainInvariantViolation


class CheckoutService:
    def __init__(self, book_repo, loan_repo):
        self._book_repo = book_repo
        self._loan_repo = loan_repo

    def checkout(self, loan_id: int, book_id: int, reader_id: int,
                 period: LoanPeriod) -> Loan:
        book = self._book_repo.get(book_id)
        if book is None:
            raise DomainInvariantViolation("Книга не найдена")

        book.take_copy()

        loan = Loan(loan_id=loan_id, book_id=book_id,
                    reader_id=reader_id, period=period)

        self._book_repo.save(book)
        self._loan_repo.save(loan)
        return loan


class ReturnService:
    def __init__(self, book_repo, loan_repo):
        self._book_repo = book_repo
        self._loan_repo = loan_repo

    def return_book(self, loan_id: int, return_date: datetime,
                    fine: Optional[Fine] = None) -> None:
        loan = self._loan_repo.get(loan_id)
        if loan is None:
            raise DomainInvariantViolation("Выдача не найдена")

        loan.close(return_date, fine)

        book = self._book_repo.get(loan.book_id)
        if book is None:
            raise DomainInvariantViolation("Книга не найдена")
        book.return_copy()

        self._loan_repo.save(loan)
        self._book_repo.save(book)