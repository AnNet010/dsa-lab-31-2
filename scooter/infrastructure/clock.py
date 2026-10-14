from datetime import datetime, timedelta


class ClockMovedBack(Exception):
    pass


class ShiftedClock:
    def __init__(self):
        self._offset = timedelta(0)

    def now(self) -> datetime:
        return datetime.now() + self._offset

    def move_to(self, moment: datetime) -> None:
        if moment < self.now():
            raise ClockMovedBack("Перевод часов назад запрещён")
        self._offset = moment - datetime.now()