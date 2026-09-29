from typing import Optional, Dict
from parking.domain.parking_spot import ParkingSpot
from parking.domain.parking_session import ParkingSession


class InMemoryParkingSpotRepository:
    def __init__(self):
        self._storage: Dict[int, ParkingSpot] = {}

    def get(self, spot_id: int) -> Optional[ParkingSpot]:
        return self._storage.get(spot_id)

    def save(self, spot: ParkingSpot) -> None:
        self._storage[spot.id] = spot


class InMemoryParkingSessionRepository:
    def __init__(self):
        self._storage: Dict[int, ParkingSession] = {}

    def get(self, session_id: int) -> Optional[ParkingSession]:
        return self._storage.get(session_id)

    def save(self, session: ParkingSession) -> None:
        self._storage[session.id] = session