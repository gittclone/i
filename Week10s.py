import paho.mqtt.client as mqtt
broker = "test.mosquitto.org"
port = 1883
topic = "home/security/intruder"
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(topic)
def on_message(client, userdata, msg):
	print(f"⚠️ ALERT: {msg.payload.decode()}")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
print("MQTT Intruder Detection Subscriber Started")
client.loop_forever()
