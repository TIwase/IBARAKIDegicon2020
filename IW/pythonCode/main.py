# -*- coding: utf-8 -*-
import os
import datetime
import requests
import serial
import RPi.GPIO as GPIO
from time import sleep
from logging import getLogger, StreamHandler, FileHandler, DEBUG

red = 17
green = 27
blue = 22
infr = 18
buzzer = 25
flag = 0
gasTH = 300
ser = serial.Serial('/dev/ttyACM0', 115200)
#ser = serial.Serial('/dev/serial0', 115200)
url = "https://notify-api.line.me/api/notify"
token = os.getenv('LINE_NOTIFY_TOKEN', None)
headers = {"Authorization" : "Bearer "+ token}

# ----------------------------------------
# 初期設定
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(infr, GPIO.IN)
    ports = [red, green, blue, buzzer]
    for port in ports:
        GPIO.setup(port, GPIO.OUT)
        GPIO.output(port,0)

# ----------------------------------------
# 赤外線検知及びLED点灯
def getInfrared():
    if GPIO.input(infr) == GPIO.HIGH:
        GPIO.output(red, 1)
        GPIO.output(green, 0)
        GPIO.output(blue, 0)
        sleep(1)

# ----------------------------------------
# ガスセンサ値取得
def getGasVal():
    rawVal = ser.readline()
    convertedVal = rawVal.strip().decode('utf-8')
    return convertedVal

# ----------------------------------------
# 5分毎にガスセンサ値のログを出力
def outGasLog(dt_now, gasVal):
    if int(dt_now.strftime('%M')) % 5 == 0:
        logfile = '\\var\\log\\mics5524\\' + dt_now.strftime('%Y-%m-%d') + '_gas.log'
        logger = getLogger(dt_now.strftime('%Y-%m-%d %H:%M %S'))    # 同じ名前を付けるとログ出力が重複されるので注意
        sh = StreamHandler()
        logger.setLevel(DEBUG)
        logger.addHandler(sh)
        fh = FileHandler(logfile)
        logger.addHandler(fh)
        logger.log(20, dt_now.strftime('%Y-%m-%d %H:%M %S') + ': [INFO] ' + gasVal)

if __name__ == '__main__':
    print("START GAS DETECTION!")
    init()
    try:
        while True:
            dt_now = datetime.datetime.now()
            gasVal = getGasVal()
            outGasLog(dt_now, gasVal)
            
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
