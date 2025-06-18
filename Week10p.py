import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# MQTT settings
broker = "test.mosquitto.org"  # Don't include square brackets or http
port = 1883
topic = "home/security/intruder"

# GPIO setup
PIR_PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)

# Connect to MQTT broker
client = mqtt.Client()
client.connect(broker, port, 60)

print("MQTT Intruder Detection Publisher Started")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Intruder detected!")
            client.publish(topic, "Intruder detected!")
            time.sleep(5)  # Delay to avoid multiple triggers
        else:
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
