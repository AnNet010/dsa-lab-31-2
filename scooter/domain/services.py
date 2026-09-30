from .scooter import Scooter
from .trip import Trip
from .value_objects import TripPeriod, Money
from .exceptions import DomainInvariantViolation


class StartTripService:
    def __init__(self, scooter_repo, trip_repo):
        self._scooter_repo = scooter_repo
        self._trip_repo = trip_repo

    def start_trip(self, trip_id: int, scooter_id: int, user_id: int,
                   period: TripPeriod) -> Trip:
        scooter = self._scooter_repo.get(scooter_id)
        if scooter is None:
            raise DomainInvariantViolation("Самокат не найден")

        scooter.start_trip()
        trip = Trip(trip_id, scooter_id, user_id, period)

        self._scooter_repo.save(scooter)
        self._trip_repo.save(trip)
        return trip


class FinishTripService:

    def __init__(self, scooter_repo, trip_repo):
        self._scooter_repo = scooter_repo
        self._trip_repo = trip_repo

    def finish_trip(self, trip_id: int, end_time, cost: Money,
                    min_cost: Money) -> None:
        trip = self._trip_repo.get(trip_id)
        if trip is None:
            raise DomainInvariantViolation("Поездка не найдена")

        trip.finish(end_time, cost, min_cost)

        scooter = self._scooter_repo.get(trip.scooter_id)
        if scooter is None:
            raise DomainInvariantViolation("Самокат не найден")
        scooter.finish_trip()

        self._trip_repo.save(trip)
        self._scooter_repo.save(scooter)