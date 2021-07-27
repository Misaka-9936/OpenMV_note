#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor, image, time
import pyb
import math
from pyb import LED

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

def Light():
    red_led.on()
    green_led.on()
    blue_led.on()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

while(True):
    clock.tick()
    # Light()
    img = sensor.snapshot()
    print(clock.fps())






