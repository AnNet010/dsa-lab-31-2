from typing import Optional, Dict, List
from scooter.domain.scooter import Scooter
from scooter.domain.trip import Trip
from scooter.domain.user import User


class InMemoryScooterRepository:
    def __init__(self):
        self._storage: Dict[int, Scooter] = {}

    def get(self, scooter_id: int) -> Optional[Scooter]:
        return self._storage.get(scooter_id)

    def save(self, scooter: Scooter) -> None:
        self._storage[scooter.id] = scooter


class InMemoryTripRepository:
    def __init__(self):
        self._storage: Dict[int, Trip] = {}

    def get(self, trip_id: int) -> Optional[Trip]:
        return self._storage.get(trip_id)

    def save(self, trip: Trip) -> None:
        self._storage[trip.id] = trip

    def all(self) -> List[Trip]:
        return list(self._storage.values())


class InMemoryUserRepository:
    def __init__(self):
        self._storage: Dict[int, User] = {}

    def get(self, user_id: int) -> Optional[User]:
        return self._storage.get(user_id)

    def save(self, user: User) -> None:
        self._storage[user.id] = user


class InMemoryPaymentGateway:
    def __init__(self, authorize_result: bool = True,
                 charge_result: bool = True):
        self._authorize_result = authorize_result
        self._charge_result = charge_result
        self._paid: Dict[int, bool] = {}

    def authorize(self, amount: float) -> bool:
        return self._authorize_result

    def is_paid(self, trip_id: int) -> bool:
        return self._paid.get(trip_id, False)

    def charge(self, trip_id: int, amount: float) -> bool:
        self._paid[trip_id] = self._charge_result
        return self._charge_result