from typing import Optional, Dict
from scooter.domain.scooter import Scooter
from scooter.domain.trip import Trip


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