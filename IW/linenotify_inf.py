# -*- coding: utf-8 -*-
import os
import datetime
import requests
#import serial
import RPi.GPIO as GPIO

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

#ser = serial.Serial('/dev/ttyACM0', 115200)
#ser = serial.Serial('/dev/serial0', 115200)

url = "https://notify-api.line.me/api/notify"
token = os.getenv('LINE_NOTIFY_TOKEN', None)
headers = {"Authorization" : "Bearer "+ token}
#infrTH = 1
flag = 0
print("START INFRARED LIGHT DETECTION!")

while True:
    dt_now = datetime.datetime.now()
    #raw_data = ser.readline()
    #infrVal = raw_data.strip().decode('utf-8')
    #print("[" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + "] " + infrVal)

    if GPIO.input(infr) == GPIO.HIGH and flag == 0:
        message = "人感検知しました、部屋に侵入者がいます。"
        payload = {"message" :  message}
        r = requests.post(url, headers = headers, params=payload)
        flag = 1
        GPIO.output(red,1)
        GPIO.output(green,0)
        GPIO.output(blue,0)

GPIO.cleanup()
ser.close()
