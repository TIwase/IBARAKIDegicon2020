# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

BeepPin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(BeepPin, GPIO.OUT)

freq = 600
pwm = GPIO.PWM(BeepPin, freq)
try:
    while True:
#        GPIO.output(BeepPin, GPIO.LOW)
#        sleep(1)
#        GPIO.output(BeepPin, GPIO.HIGH)
#        sleep(1)
# PWMによる制御
        pwm.start(50)
        sleep(3)
        pwm.stop()
        sleep(1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()

