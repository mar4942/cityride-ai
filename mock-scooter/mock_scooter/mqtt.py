"""MQTT publisher — publishes scooter state changes to the broker."""

import json
import logging
from typing import Optional

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

DEFAULT_BROKER = "localhost"
DEFAULT_PORT = 1883


class MqttPublisher:
    """Thin wrapper around paho-mqtt that publishes state as JSON."""

    def __init__(self, broker: str = DEFAULT_BROKER, port: int = DEFAULT_PORT) -> None:
        self._client = mqtt.Client()
        self._broker = broker
        self._port = port
        self._connected = False

    def connect(self) -> None:
        """Connect to the MQTT broker (non‑blocking)."""
        try:
            self._client.connect_async(self._broker, self._port)
            self._client.loop_start()
            self._connected = True
            logger.info("MQTT publisher connected to %s:%s", self._broker, self._port)
        except Exception as exc:
            logger.warning("MQTT connection failed (%s); messages will be dropped", exc)
            self._connected = False

    def publish(self, scooter_id: str, state: dict) -> None:
        """Publish a state dict on ``scooter/<id>/state``."""
        if not self._connected:
            logger.debug("MQTT not connected — skipping publish for %s", scooter_id)
            return
        topic = f"scooter/{scooter_id}/state"
        payload = json.dumps(state, ensure_ascii=False)
        self._client.publish(topic, payload, qos=1)
        logger.info("Published to %s: %s", topic, payload)

    def disconnect(self) -> None:
        """Disconnect from the broker."""
        if self._connected:
            self._client.loop_stop()
            self._client.disconnect()
            self._connected = False
            logger.info("MQTT publisher disconnected")