#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

# AprilTag 推荐使用 TAG36H11
# 只有 OpenMV Cam M7 可以

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
sensor.set_framesize(sensor.QQVGA)              # 若太大，内存会不够
sensor.skip_frames(10)
sensor.set_auto_gain(False)                     # 这两项必须关闭
sensor.set_auto_whitebal(False)

clock = time.clock()

while(True):
    clock.tick()
    Light()
    img = sensor.snapshot()
    for tag in img.find_apriltags():            # 默认是TAG36H11，无families
        img.draw_rectangle(tag.rect(), color=(255,0,0))
        img.draw_cross(tag.cx(), tag.cy(), color=(0,255,0))
        degress = 180 * tag.rotation() / math.pi
        print(tag.id(), degress)

# 我们可以用这个标签计算空间位置————即定位、测距







