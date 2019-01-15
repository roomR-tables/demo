import os
from configparser import ConfigParser
import json
import logging
import paho.mqtt.client as mqtt
import sqlite3


def runApp():
    log = logging.basicConfig()
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "../config.ini"))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(mqtt_client, userdata, flags, rc):
        mqtt_client.subscribe("cc/cmd")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(mqtt_client, userdata, msg):
        # Create new SQLite3 connection for this thread
        conn = sqlite3.connect('cc.db')
        conn.row_factory = sqlite3.Row

        payload = msg.payload.decode("utf-8")

        try:
            msg_json = json.loads(payload)
        except json.JSONDecodeError as e:
            log.error("Error when decoding json: %s", e)
            return

        """
        A JSON message in the following response is expected:
        { "cmd": "request_status", "payload": ... }
        """
        if msg.topic == 'cc/cmd':
            if msg_json["cmd"] == "request_status":
                try:
                    with conn:
                        cur = conn.cursor()
                        cur.execute("SELECT `status` FROM `settings`")
                        conn.commit()

                        mqtt_client.publish(topic="cc/status", payload=cur.fetchone()[0])
                except sqlite3.Error as e:
                    print(e)

            if msg_json["cmd"] == "move":
                print("move!")
                # Do some stuff to calculate the movement from current position to requested

        conn.close()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(config.get("mqtt", "host"), int(config.get("mqtt", "port")), 60)
    except ConnectionError as e:
        log.error("Error when connecting to the MQTT broker: %s", e)
        exit(1)

    client.loop_start()

    while True:
        continue
