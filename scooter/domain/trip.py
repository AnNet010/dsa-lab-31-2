from datetime import datetime
from typing import Optional
from .exceptions import DomainInvariantViolation
from .value_objects import TripPeriod, Money


class Trip:
    def __init__(self, trip_id: int, scooter_id: int, user_id: int,
                 period: TripPeriod):
        self._id = trip_id
        self._scooter_id = scooter_id
        self._user_id = user_id
        self._period = period
        self._cost: Optional[Money] = None
        self._is_finished = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def scooter_id(self) -> int:
        return self._scooter_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    def finish(self, end_time: datetime, cost: Money, min_cost: Money):
        if self._is_finished:
            raise DomainInvariantViolation("Поездка уже завершена")
        if end_time < self._period.start_time:
            raise DomainInvariantViolation(
                "Время окончания не может быть раньше времени начала"
            )
        if cost.amount < min_cost.amount:
            raise DomainInvariantViolation(
                "Стоимость не может быть меньше минимальной"
            )
        self._period = TripPeriod(self._period.start_time, end_time)
        self._cost = cost
        self._is_finished = True

    @classmethod
    def restore(cls, trip_id: int, scooter_id: int, user_id: int,
                period: TripPeriod, cost: Optional[Money] = None,
                is_finished: bool = False) -> "Trip":
        trip = cls(trip_id, scooter_id, user_id, period)
        trip._cost = cost
        trip._is_finished = is_finished

        if is_finished and cost is None:
            raise DomainInvariantViolation(
                "Завершённая поездка должна иметь стоимость"
            )
        return trip