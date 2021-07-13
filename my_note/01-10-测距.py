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

yellow_threshold = (64, 85, -7, 12, 27, 68)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)      # 为了速度和帧率，用QQVGA
sensor.skip_frames(10)                  # 让新设置生效
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()                    # 追踪FPS

K = 5000        # 自己计算
# K = 物体放置的距离 * 打印出的物体像素大小

while(True):
    clock.tick()
    Light()
    img = sensor.snapshot()

    blobs = img.find_blobs([yellow_threshold])
    for blob in blobs:
        if len(blobs) == 1:
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            center_x = blob[5]
            center_y = blob[6]
            img.draw_rectangle([x, y, width, height])           # rect
            img.draw_cross(center_x, center_y)                  # cx, cy
            Lm = (width+height)/2
            length = K/Lm
            print(length, clock.fps())





