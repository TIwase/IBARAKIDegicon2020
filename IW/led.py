import RPi.GPIO as GPIO
from time import sleep

red = 17
green = 27
blue = 22
GPIO.setmode(GPIO.BCM)
ports = [red, green, blue]
for port in ports:
	GPIO.setup(port, GPIO.OUT)

try:
        while True:
		GPIO.output(red,1)
		GPIO.output(green,1)
		GPIO.output(blue,1)
                sleep(1)
		GPIO.output(red,0)
		GPIO.output(green,1)
		GPIO.output(blue,1)
                sleep(1)
		GPIO.output(red,1)
		GPIO.output(green,1)
		GPIO.output(blue,0)
                sleep(1)

except KeyboardInterrupt:
        pass

GPIO.cleanup()
