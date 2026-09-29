class DomainError(Exception):
    pass


class DomainInvariantViolation(DomainError):
    pass


class InvalidValueObject(DomainError):
    pass