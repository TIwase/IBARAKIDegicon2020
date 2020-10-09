# -*- coding: utf-8 -*-
import os
import datetime
import requests
import serial

ser = serial.Serial('/dev/ttyACM0', 115200)
#ser = serial.Serial('/dev/serial0', 115200)

url = "https://notify-api.line.me/api/notify"
token = os.getenv('LINE_NOTIFY_TOKEN', None)
headers = {"Authorization" : "Bearer "+ token}
flag = 0
print("START GAS DETECTION!")

while True:
    dt_now = datetime.datetime.now()
    raw_data = ser.readline()
    gas_value = raw_data.strip().decode('utf-8')
    print("[" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + "] " + gas_value)
    if int(gas_value) > 20 and flag == 0:
        message = "ガスセンサ値の閾値超過を検知しました。ガス漏れしている可能性があります。"
        payload = {"message" :  message}
        r = requests.post(url, headers = headers, params=payload)
        flag = 1
ser.close()
