from typing import Optional, Dict, List
from rooms.domain.room import Room
from rooms.domain.booking import Booking


class InMemoryRoomRepository:
    def __init__(self):
        self._storage: Dict[int, Room] = {}

    def get(self, room_id: int) -> Optional[Room]:
        return self._storage.get(room_id)

    def save(self, room: Room) -> None:
        self._storage[room.id] = room


class InMemoryBookingRepository:
    def __init__(self):
        self._storage: Dict[int, Booking] = {}

    def get(self, booking_id: int) -> Optional[Booking]:
        return self._storage.get(booking_id)

    def save(self, booking: Booking) -> None:
        self._storage[booking.id] = booking

    def list_by_room(self, room_id: int) -> List[Booking]:
        return [b for b in self._storage.values() if b.room_id == room_id]