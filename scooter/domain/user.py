from datetime import datetime
from typing import List
from .events import AccountBlocked


class User:
    def __init__(self, user_id: int, has_debt: bool = False,
                 is_blocked: bool = False):
        self._id = user_id
        self._has_debt = has_debt
        self._is_blocked = is_blocked
        self._events: List = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def has_debt(self) -> bool:
        return self._has_debt

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    @property
    def events(self) -> tuple:
        return tuple(self._events)

    def check_debt(self) -> bool:
        return self._has_debt

    def block(self, now: datetime) -> None:
        self._is_blocked = True
        self._events.append(AccountBlocked(self._id, now))