# -*- coding: utf-8 -*-
import os
import datetime
import requests
import serial
import RPi.GPIO as GPIO
from time import sleep

red = 17
green = 27
blue = 22
infr = 18
buzzer = 25
ser = serial.Serial('/dev/ttyACM0', 115200)
#ser = serial.Serial('/dev/serial0', 115200)
url = "https://notify-api.line.me/api/notify"
token = os.getenv('LINE_NOTIFY_TOKEN', None)
headers = {"Authorization" : "Bearer "+ token}
flag = 0
gasTH = 300

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(infr, GPIO.IN)
    ports = [red, green, blue, buzzer]
    for port in ports:
        GPIO.setup(port, GPIO.OUT)
        GPIO.output(port,0)

def getInfrared():
    if GPIO.input(infr) == GPIO.HIGH:
        GPIO.output(red, 1)
        GPIO.output(green, 0)
        GPIO.output(blue, 0)
        sleep(1)
        
if __name__ == '__main__':
    print("START GAS DETECTION!")
    init()
    try:
        while True:
            dt_now = datetime.datetime.now()
            raw_data = ser.readline()
            gasVal = raw_data.strip().decode('utf-8')
            if int(dt_now.strftime('%M')) % 5 == 0:
                print("[" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + "] " + gasVal)
            if int(gasVal) > gasTH and GPIO.input(infr) == GPIO.HIGH and flag == 0:
                getInfrared()
                message = "ガスセンサ値の閾値超過を検知しました。ガス漏れしている可能性があります。"
                payload = {"message" :  message}
                r = requests.post(url, headers = headers, params=payload)
                flag = 1

    except KeyboardInterrupt:
        pass

    ser.close()
    GPIO.cleanup()
