import time
import math
from gpiozero import MCP3208

adc0 = MCP3208(channel=0)

while True:
	print(adc0.value)
	time.sleep(1)


