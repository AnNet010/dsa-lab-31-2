from datetime import datetime
from .parking_spot import ParkingSpot
from .parking_session import ParkingSession
from .value_objects import Money
from .exceptions import DomainInvariantViolation


class ParkingService:
    def __init__(self, spot_repo, session_repo):
        self._spot_repo = spot_repo
        self._session_repo = session_repo

    def enter(self, session_id: int, spot_id: int, car_id: int,
              entry_time: datetime) -> ParkingSession:
        spot = self._spot_repo.get(spot_id)
        if spot is None:
            raise DomainInvariantViolation("Место не найдено")

        spot.occupy()
        session = ParkingSession(session_id, spot_id, car_id, entry_time)

        self._spot_repo.save(spot)
        self._session_repo.save(session)
        return session

    def exit(self, session_id: int, exit_time: datetime,
             cost: Money) -> None:
        session = self._session_repo.get(session_id)
        if session is None:
            raise DomainInvariantViolation("Сессия не найдена")

        session.close(exit_time, cost)

        spot = self._spot_repo.get(session.spot_id)
        if spot is None:
            raise DomainInvariantViolation("Место не найдено")
        spot.free()

        self._session_repo.save(session)
        self._spot_repo.save(spot)