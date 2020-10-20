# -*- coding: utf-8 -*-
import os
import datetime
import requests
import serial
import RPi.GPIO as GPIO
from time import sleep
from logging import getLogger, StreamHandler, FileHandler, DEBUG

red = 22
green = 17
blue = 27
infr = 13
ports = [red, green, blue]
buzzer = 25
flag = 0
gasTH = 300
ser = serial.Serial('/dev/ttyACM0', 115200)
#ser = serial.Serial('/dev/serial0', 115200)
url = "https://notify-api.line.me/api/notify"
token = os.getenv('LINE_NOTIFY_TOKEN', None)
headers = {"Authorization" : "Bearer "+ token}
logpath = os.getcwd()
detecTime = ''

# ----------------------------------------
# 初期設定
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(infr, GPIO.IN)
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
    elif GPIO.input(infr) == GPIO.LOW:
        for port in ports:
            GPIO.output(port,0)
        sleep(1)

# ----------------------------------------
# ガスセンサ値取得
def getGasVal():
    rawVal = ser.readline()
    convVal = int(rawVal.strip().decode('utf-8'))
    return convVal

# ----------------------------------------
# 5分毎にガスセンサ値のログを出力
def outGasLog(dt_now, gasVal):
    if int(dt_now.strftime('%M')) % 5 == 0 and int(dt_now.strftime('%S'))  == 0:
        logfile = logpath + '/gaslog/' + dt_now.strftime('%Y-%m-%d') + '_gas.log'
        logger = getLogger(dt_now.strftime('%Y-%m-%d %H:%M %S'))    # 同じ名前を付けるとログ出力が重複されるので注意
        sh = StreamHandler()
        logger.setLevel(DEBUG)
        logger.addHandler(sh)
        fh = FileHandler(logfile)
        logger.addHandler(fh)
        if gasVal < gasTH:
            logger.log(20, dt_now.strftime('%Y-%m-%d %H:%M %S') + ': [INFO] ' + str(gasVal))
        elif gasVal > gasTH:
            logger.log(30, dt_now.strftime('%Y-%m-%d %H:%M %S') + ': [WARN] ' + str(gasVal) + ' The current gas value exceeded the threshold ')

if __name__ == '__main__':
    print("START GAS DETECTION!")
    init()
    try:
        while True:
            dt_now = datetime.datetime.now()
            gasVal = getGasVal()
            outGasLog(dt_now, gasVal)
            getInfrared()
            if detecTime != dt_now.strftime('%M'):
                flag = 0

            if gasVal > gasTH and GPIO.input(infr) == GPIO.HIGH and flag == 0:
                message = "ガスセンサ値の閾値超過を検知しました。ガス漏れしている可能性があります。"
                payload = {"message" :  message}
                r = requests.post(url, headers = headers, params=payload)
                detecTime = dt_now.strftime('%M')
                flag = 1

    except KeyboardInterrupt:
        pass

    ser.close()
    GPIO.cleanup()
