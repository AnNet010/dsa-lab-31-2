from library.domain.exceptions import DomainInvariantViolation


class Book:
    def __init__(self, book_id: int, name: str, publisher: str, year: int,
                 total_copies: int, available_copies: int = None):
        self._id = book_id
        self._name = name
        self._publisher = publisher
        self._year = year
        self._total_copies = total_copies
        self._available_copies = available_copies if available_copies is not None else total_copies

    @property
    def id(self) -> int:
        return self._id

    @property
    def available_copies(self) -> int:
        return self._available_copies

    def can_be_taken(self) -> bool:
        return self._available_copies > 0

    def take_copy(self):
        if not self.can_be_taken():
            raise DomainInvariantViolation("Нет свободных экземпляров")
        self._available_copies -= 1

    def return_copy(self):
        if self._available_copies >= self._total_copies:
            raise DomainInvariantViolation("Нельзя вернуть больше, чем есть")
        self._available_copies += 1

    @classmethod
    def restore(cls, book_id: int, name: str, publisher: str, year: int,
                total_copies: int, available_copies: int) -> "Book":
        book = cls(book_id, name, publisher, year, total_copies, available_copies)
        if book._available_copies > book._total_copies:
            raise DomainInvariantViolation("Доступных экземпляров больше, чем всего")
        return book