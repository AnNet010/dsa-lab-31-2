import pytest
from datetime import datetime

from library.domain.value_objects import LoanPeriod, Fine
from library.domain.book import Book
from library.domain.loan import Loan
from library.domain.services import CheckoutService, ReturnService
from library.domain.exceptions import DomainInvariantViolation, InvalidValueObject
from library.infrastructure.in_memory import InMemoryBookRepository, InMemoryLoanRepository


def test_book_no_available_copies():
    book = Book(1, "Мастер и Маргарита", "АСТ", 2020,
                total_copies=1, available_copies=0)
    with pytest.raises(DomainInvariantViolation):
        book.take_copy()


def test_loan_cannot_be_closed_twice():
    period = LoanPeriod(datetime(2026, 1, 1), datetime(2026, 1, 10))
    loan = Loan(1, 1, 1, period)
    loan.close(datetime(2026, 1, 5))
    with pytest.raises(DomainInvariantViolation):
        loan.close(datetime(2026, 1, 6))


def test_checkout_service():
    book_repo = InMemoryBookRepository()
    loan_repo = InMemoryLoanRepository()

    book = Book(1, "Мастер и Маргарита", "АСТ", 2020,
                total_copies=3, available_copies=3)
    book_repo.save(book)

    service = CheckoutService(book_repo, loan_repo)
    period = LoanPeriod(datetime(2026, 1, 1), datetime(2026, 1, 10))
    loan = service.checkout(loan_id=1, book_id=1, reader_id=1, period=period)

    assert book.available_copies == 2
    assert loan_repo.get(1) is not None