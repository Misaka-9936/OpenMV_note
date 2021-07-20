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

red_threshold = (45, 61, 14, 61, -6, 40)
yellow_threshold = (73, 95, -20, 10, 20, 66)

red_color_code = 1          # code = 2^0 = 1 = 0001H
green_color_code = 2        # code = 2^1 = 2 = 0010H
blue_color_code = 4         # code = 2^2 = 4 = 0100H
black_color_code = 8        # code = 2^3 = 8 = 1000H

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

while(True):
    clock.tick()
    Light()
    img = sensor.snapshot()

    blobs = img.find_blobs([red_threshold,yellow_threshold], area_threshold=200, merge=True)
    if blobs:
        for blob in blobs:
            x = blob[0]             # 赋值官方给的色块对象
            y = blob[1]
            width = blob[2]
            height = blob[3]
            cx = blob[5]
            cy = blob[6]
            color_code = blob[8]    # blob.code()返回的值：1，2，4，8，与前面传入blobs的阈值顺序有关

            img.draw_rectangle([x, y, width, height])
            img.draw_cross(cx, cy)

            print("color_code =", color_code)






