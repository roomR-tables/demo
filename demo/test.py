import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

# msg = subscribe.simple("cc/status", hostname="localhost")
publish.single("cc/cmd", '{"cmd": "request_status", "payload": ""}', hostname="localhost", port=1883)
