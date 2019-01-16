import os
from configparser import ConfigParser
import json
import logging
import time

from RF24 import *
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import sqlite3

from nrf import Nrf

# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_22, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
radio.begin()
radio.enableDynamicPayloads()
radio.printDetails()

pipes = [bytearray("arduino_read", "utf-8"), bytearray("pi_read", "utf-8")]

# Do not use 0 as reading pipe! This pipe is already in use as writing pipe
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.startListening()

nrf = Nrf(radio)


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
        message = nrf.read_message()

        if message is not None:
            print(message)

        # Blocking call until a message is received
        #msg = subscribe.simple("cc/cmd", hostname=config.get("mqtt", "host"), port=int(config.get("mqtt", "port")))
        #payload = msg.payload.decode("utf-8")

        #try:
        #    msg_json = json.loads(payload)
        #except json.JSONDecodeError as e:
        #    log.error("Error when decoding json: %s", e)
        #    continue

        #if msg_json["cmd"] == "move":
        #print("MOVE")
