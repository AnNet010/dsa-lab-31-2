from flask import jsonify
from scooter.domain.exceptions import (
    TransitionNotAllowed, DomainInvariantViolation,
    InvalidValueObject, GatewayUnresolved,
)
from scooter.infrastructure.clock import ClockMovedBack


def register_error_handlers(app):
    @app.errorhandler(TransitionNotAllowed)
    def handle_transition_not_allowed(e):
        return jsonify({
            "error": "transition_not_allowed",
            "message": str(e),
        }), 409

    @app.errorhandler(DomainInvariantViolation)
    def handle_invariant(e):
        return jsonify({
            "error": "invariant_violation",
            "message": str(e),
        }), 422

    @app.errorhandler(InvalidValueObject)
    def handle_value_object(e):
        return jsonify({
            "error": "invalid_value_object",
            "message": str(e),
        }), 422

    @app.errorhandler(ClockMovedBack)
    def handle_clock_moved_back(e):
        return jsonify({
            "error": "clock_moved_back",
            "message": str(e),
        }), 422

    @app.errorhandler(GatewayUnresolved)
    def handle_gateway_unresolved(e):
        return jsonify({
            "error": "gateway_unresolved",
            "message": str(e),
        }), 500