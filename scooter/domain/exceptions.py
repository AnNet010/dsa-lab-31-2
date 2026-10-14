class DomainError(Exception):
    pass


class DomainInvariantViolation(DomainError):
    pass


class InvalidValueObject(DomainError):
    pass


class TransitionNotAllowed(DomainError):

    def __init__(self, state: str, event: str):
        super().__init__(
            f"Событие '{event}' недопустимо в состоянии «{state}»"
        )
        self.state = state
        self.event = event


class GatewayUnresolved(DomainError):
    pass