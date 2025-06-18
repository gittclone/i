import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)   # LED 1 (Low Temp - Cold)
GPIO.setup(10, GPIO.OUT)  # LED 2 (Normal Temp)
GPIO.setup(12, GPIO.OUT)  # LED 3 (High Temp - Hot)

# Initially turn off all LEDs
GPIO.output(8, GPIO.LOW)
GPIO.output(10, GPIO.LOW)
GPIO.output(12, GPIO.LOW)

# Use DHT11 sensor on BCM pin 4 (which is BOARD pin 7)
sensor = Adafruit_DHT.DHT11
pin = 4  # BCM pin number

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print('Temp: {0:0.1f}°C  Humidity: {1:0.1f}%'.format(temperature, humidity))
            temp_int = int(temperature)

            if temp_int < 20:
                GPIO.output(8, GPIO.HIGH)   # Cold
                GPIO.output(10, GPIO.LOW)
                GPIO.output(12, GPIO.LOW)
            elif 20 <= temp_int < 30:
                GPIO.output(10, GPIO.HIGH)  # Normal
                GPIO.output(8, GPIO.LOW)
                GPIO.output(12, GPIO.LOW)
            else:  # temp_int >= 30
                GPIO.output(12, GPIO.HIGH)  # Hot
                GPIO.output(10, GPIO.LOW)
                GPIO.output(8, GPIO.LOW)
        else:
            print("Failed to retrieve data from DHT sensor")

        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.cleanup()
