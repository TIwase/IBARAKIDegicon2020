import RPi.GPIO as GPIO
from time import sleep

BeepPin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(BeepPin, GPIO.OUT)

pwm = GPIO.PWM(BeepPin, 600)

pwm.start(50)
sleep(3)
pwm.stop()

GPIO.cleanup()

