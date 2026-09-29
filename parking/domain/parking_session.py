from typing import Optional
from datetime import datetime
from .exceptions import DomainInvariantViolation
from .value_objects import ParkingPeriod, Money


class ParkingSession:
    def __init__(self, session_id: int, spot_id: int, car_id: int,
                 entry_time: datetime):
        self._id = session_id
        self._spot_id = spot_id
        self._car_id = car_id
        self._entry_time = entry_time
        self._exit_time: Optional[datetime] = None
        self._cost: Optional[Money] = None
        self._is_closed = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def spot_id(self) -> int:
        return self._spot_id

    @property
    def car_id(self) -> int:
        return self._car_id

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    def close(self, exit_time: datetime, cost: Money):
        if self._is_closed:
            raise DomainInvariantViolation("Сессия уже закрыта")
        if exit_time < self._entry_time:
            raise DomainInvariantViolation(
                "Время выезда не может быть раньше времени въезда"
            )
        self._exit_time = exit_time
        self._cost = cost
        self._is_closed = True

    @classmethod
    def restore(cls, session_id: int, spot_id: int, car_id: int,
                entry_time: datetime, exit_time: Optional[datetime] = None,
                cost: Optional[Money] = None,
                is_closed: bool = False) -> "ParkingSession":
        session = cls(session_id, spot_id, car_id, entry_time)
        session._exit_time = exit_time
        session._cost = cost
        session._is_closed = is_closed

        if is_closed and exit_time is None:
            raise DomainInvariantViolation(
                "Закрытая сессия должна иметь время выезда"
            )
        return session