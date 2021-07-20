import sensor, image, time
import pyb
from pyb import UART
from pyb import LED

uart = UART(3, 115200)

while(True):
    uart.write("Hello World!\r")
    time.sleep_ms(1000)





