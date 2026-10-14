from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TripReserved:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class TripReservationExpired:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class TripRejected:
    trip_id: int
    reason: str
    occurred_at: datetime


@dataclass(frozen=True)
class TripStarted:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class TripPaused:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class TripResumed:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class TripFinished:
    trip_id: int
    cost: float
    occurred_at: datetime


@dataclass(frozen=True)
class TripRejectedInZone:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class LongTripNotification:
    trip_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class AccountBlocked:
    user_id: int
    occurred_at: datetime