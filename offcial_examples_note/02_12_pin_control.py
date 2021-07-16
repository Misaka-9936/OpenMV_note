# Pin Control Example
#
# This example shows how to use the I/O pins in GPIO mode on your OpenMV Cam.

from pyb import Pin

# Connect a switch to pin 0 that will pull it low when the switch is closed.
# Pin 1 will then light up.
# 连接一个开关到Pin0，当开关闭合的时候，引脚置低，然后Pin1会点亮
pin0 = Pin('P0', Pin.IN, Pin.PULL_UP)
pin1 = Pin('P1', Pin.OUT_PP, Pin.PULL_NONE)

while(True):
    pin1.value(not pin0.value())
