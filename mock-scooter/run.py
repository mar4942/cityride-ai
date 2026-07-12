#!/usr/bin/env python3
"""Entry point — starts the mock-scooter REST API server.

Usage
-----
    python run.py                    # default: port 5000, MQTT on localhost:1883
    python run.py --port 5001        # custom port
    python run.py --no-mqtt          # run without MQTT
    python run.py --mqtt-broker 10.0.0.5 --mqtt-port 1883
"""

import argparse
import logging

from mock_scooter.app import create_app
from mock_scooter.mqtt import MqttPublisher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mock e-scooter REST API")
    parser.add_argument("--port", type=int, default=5000, help="HTTP port (default: 5000)")
    parser.add_argument("--mqtt-broker", default="localhost", help="MQTT broker host")
    parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--no-mqtt", action="store_true", help="Disable MQTT publishing")
    args = parser.parse_args()

    mqtt_publisher: MqttPublisher | None = None
    if not args.no_mqtt:
        mqtt_publisher = MqttPublisher(broker=args.mqtt_broker, port=args.mqtt_port)
        mqtt_publisher.connect()

    app = create_app(mqtt_publisher=mqtt_publisher)

    logger.info("Starting mock-scooter on port %d (MQTT: %s)", args.port, "disabled" if args.no_mqtt else "enabled")
    app.run(host="0.0.0.0", port=args.port, debug=False)


if __name__ == "__main__":
    main()