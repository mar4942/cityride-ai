"""Flask REST API — exposes endpoints to control a simulated scooter."""

import logging
from typing import Optional

from flask import Flask, jsonify, request

from .scooter import Scooter
from .mqtt import MqttPublisher

logger = logging.getLogger(__name__)


def create_app(
    scooter: Optional[Scooter] = None,
    mqtt_publisher: Optional[MqttPublisher] = None,
) -> Flask:
    """Build and return a configured Flask application.

    Parameters
    ----------
    scooter : Scooter, optional
        The scooter instance to control.  A default one is created if omitted.
    mqtt_publisher : MqttPublisher, optional
        MQTT publisher.  If omitted, state changes are not broadcast.
    """
    app = Flask(__name__)

    if scooter is None:
        scooter = Scooter(scooter_id="mock-001")

    # Wire up the change callback so every mutation publishes an MQTT message.
    if mqtt_publisher is not None:
        def on_change(s: Scooter) -> None:
            mqtt_publisher.publish(s.scooter_id, s.to_dict())
        scooter.on_change = on_change

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.route("/state", methods=["GET"])
    def get_state():
        """Return the current scooter state."""
        return jsonify(scooter.to_dict())

    @app.route("/set-battery", methods=["POST"])
    def set_battery():
        """Set battery level.

        JSON body: {"level": <float 0‑100>}
        """
        data = request.get_json(force=True)
        level = float(data["level"])
        scooter.set_battery(level)
        return jsonify(scooter.to_dict())

    @app.route("/lock", methods=["POST"])
    def lock():
        """Lock the scooter."""
        scooter.set_locked(True)
        return jsonify(scooter.to_dict())

    @app.route("/unlock", methods=["POST"])
    def unlock():
        """Unlock the scooter."""
        scooter.set_locked(False)
        return jsonify(scooter.to_dict())

    @app.route("/set-position", methods=["POST"])
    def set_position():
        """Set geographic position.

        JSON body: {"lat": <float>, "lng": <float>}
        """
        data = request.get_json(force=True)
        lat = float(data["lat"])
        lng = float(data["lng"])
        scooter.set_position(lat, lng)
        return jsonify(scooter.to_dict())

    return app