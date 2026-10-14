from .exceptions import TransitionNotAllowed, DomainInvariantViolation


class TripState:
    name: str = ""
    allowed: frozenset[str] = frozenset()

    def pay_authorized(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "pay_authorized")

    def pay_failed(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "pay_failed")

    def expire(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "expire")

    def start(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "start")

    def pause(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "pause")

    def resume(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "resume")

    def finish(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "finish")

    def reject_zone(self, trip: "Trip") -> "TripState":
        raise TransitionNotAllowed(self.name, "reject_zone")


class Reserved(TripState):
    name = "Забронирована"
    allowed = frozenset({"pay_authorized", "pay_failed", "expire"})

    def pay_authorized(self, trip: "Trip") -> "TripState":
        return Active()

    def pay_failed(self, trip: "Trip") -> "TripState":
        return NotStarted()

    def expire(self, trip: "Trip") -> "TripState":
        return Cancelled()


class Active(TripState):
    name = "Активна"
    allowed = frozenset({"pause", "finish", "reject_zone"})

    def pause(self, trip: "Trip") -> "TripState":
        return Paused()

    def finish(self, trip: "Trip") -> "TripState":
        if not trip.is_in_allowed_zone:
            raise DomainInvariantViolation(
                "Нельзя завершить поездку вне разрешённой зоны"
            )
        return Finished()

    def reject_zone(self, trip: "Trip") -> "TripState":
        return RejectedInZone()


class Paused(TripState):
    name = "На паузе"
    allowed = frozenset({"resume", "finish", "reject_zone"})

    def resume(self, trip: "Trip") -> "TripState":
        return Active()

    def finish(self, trip: "Trip") -> "TripState":
        if not trip.is_in_allowed_zone:
            raise DomainInvariantViolation(
                "Нельзя завершить поездку вне разрешённой зоны"
            )
        return Finished()

    def reject_zone(self, trip: "Trip") -> "TripState":
        return RejectedInZone()


class Finished(TripState):
    name = "Завершена"


class RejectedInZone(TripState):
    name = "Отклонена"


class Cancelled(TripState):
    name = "Отменена"


class NotStarted(TripState):
    name = "Не начата"