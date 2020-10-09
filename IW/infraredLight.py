import RPi.GPIO as GPIO
from time import sleep

red = 17
green = 27
blue = 22
infr = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(infr, GPIO.IN)

ports = [red, green, blue]
for port in ports:
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port,0)

try:
    while True:

        if(GPIO.input(infr) == GPIO.HIGH):
            GPIO.output(red,1)
            GPIO.output(green,0)
            GPIO.output(blue,0)
            print(GPIO.input(infr))
            sleep(1)

        elif(GPIO.input(infr) == GPIO.LOW):
            for port in ports:	
                GPIO.output(port,0)
            print(GPIO.input(infr))
            sleep(1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
