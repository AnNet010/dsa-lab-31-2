from typing import Optional, Dict
from library.domain.book import Book
from library.domain.loan import Loan


class InMemoryBookRepository:
    def __init__(self):
        self._storage: Dict[int, Book] = {}

    def get(self, book_id: int) -> Optional[Book]:
        return self._storage.get(book_id)

    def save(self, book: Book) -> None:
        self._storage[book.id] = book


class InMemoryLoanRepository:
    def __init__(self):
        self._storage: Dict[int, Loan] = {}

    def get(self, loan_id: int) -> Optional[Loan]:
        return self._storage.get(loan_id)

    def save(self, loan: Loan) -> None:
        self._storage[loan.id] = loan