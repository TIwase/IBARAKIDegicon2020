import serial
ser = serial.Serial('/dev/ttyACM0', 115200)
#ser = serial.Serial('/dev/serial0', 115200)
while True:
    raw_data = ser.readline()
    print(raw_data.strip().decode('utf-8'))
ser.close()
