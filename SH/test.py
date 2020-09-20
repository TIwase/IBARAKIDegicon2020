import RPi.GPIO as GPIO
from time import sleep

Led_red_pin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup(Led_red_pin, GPIO.OUT)

try:
	while True:
		if(GPIO.input(18) == GPIO.HIGH):
	        	GPIO.output(Led_red_pin, GPIO.HIGH)
			print GPIO.input(18)
			sleep(1)
		else:
			GPIO.output(Led_red_pin, GPIO.LOW)
			sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
