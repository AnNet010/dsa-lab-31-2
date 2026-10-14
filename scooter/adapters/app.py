import os
from datetime import datetime
from flask import Flask, request, jsonify

from scooter.domain.services import ScooterProcess
from scooter.domain.value_objects import Money, Battery
from scooter.domain.scooter import Scooter
from scooter.domain.user import User
from scooter.infrastructure.in_memory import (
    InMemoryScooterRepository, InMemoryTripRepository,
    InMemoryUserRepository, InMemoryPaymentGateway,
)
from scooter.infrastructure.clock import ShiftedClock
from scooter.adapters.errors import register_error_handlers


def create_app():
    app = Flask(__name__)

    scooter_repo = InMemoryScooterRepository()
    trip_repo = InMemoryTripRepository()
    user_repo = InMemoryUserRepository()
    payment = InMemoryPaymentGateway()
    clock = ShiftedClock()

    scooter_repo.save(Scooter(1, Battery(80)))
    user_repo.save(User(1, has_debt=False))

    process = ScooterProcess(
        scooter_repo, trip_repo, user_repo, payment, clock
    )

    app.config["process"] = process
    app.config["clock"] = clock
    app.config["trip_repo"] = trip_repo
    app.config["scooter_repo"] = scooter_repo
    app.config["user_repo"] = user_repo

    register_error_handlers(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/trips/<int:trip_id>")
    def get_trip(trip_id):
        trip = trip_repo.get(trip_id)
        if trip is None:
            return jsonify({
                "error": "not_found",
                "message": f"Поездка {trip_id} не найдена",
            }), 404
        return jsonify({
            "id": trip.id,
            "status": trip.status,
            "allowed_events": sorted(trip.allowed_events),
            "events": [
                {"type": type(e).__name__, **e.__dict__}
                for e in trip.events
            ],
        })

    @app.post("/trips/<int:trip_id>/reserve")
    def reserve(trip_id):
        data = request.get_json() or {}
        start_time = (
            datetime.fromisoformat(data["start_time"])
            if "start_time" in data else clock.now()
        )
        process.reserve_scooter(
            trip_id=trip_id,
            scooter_id=data["scooter_id"],
            user_id=data["user_id"],
            start_time=start_time,
        )
        return jsonify({"status": "reserved"}), 201

    @app.post("/trips/<int:trip_id>/start")
    def start(trip_id):
        data = request.get_json() or {}
        process.start_trip(
            trip_id=trip_id, scooter_id=data["scooter_id"]
        )
        return jsonify({"status": "started"})

    @app.post("/trips/<int:trip_id>/pause")
    def pause(trip_id):
        process.pause_trip(trip_id)
        return jsonify({"status": "paused"})

    @app.post("/trips/<int:trip_id>/resume")
    def resume(trip_id):
        process.resume_trip(trip_id)
        return jsonify({"status": "resumed"})

    @app.post("/trips/<int:trip_id>/finish")
    def finish(trip_id):
        data = request.get_json() or {}
        cost = Money(float(data.get("cost", 0)))
        is_in_zone = bool(data.get("is_in_zone", False))
        process.finish_trip(trip_id, cost, is_in_zone)
        return jsonify({"status": "finished"})

    @app.post("/internal/tick")
    def tick():
        data = request.get_json() or {}
        if "now" in data:
            moment = datetime.fromisoformat(data["now"])
            clock.move_to(moment)
        now = clock.now()
        process.on_reservation_expired(now)
        process.on_long_trip(now)
        return jsonify({"now": now.isoformat()})

    @app.post("/users/<int:user_id>/debt")
    def set_debt(user_id):
        user = user_repo.get(user_id)
        if user is None:
            return jsonify({"error": "not_found"}), 404
        user._has_debt = True
        user_repo.save(user)
        return jsonify({"status": "debt_set"})

    return app