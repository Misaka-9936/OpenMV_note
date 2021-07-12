#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor, image, time, pyb
from pyb import LED

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

red_thresholds = (23, 50, 14, 48, -8, 39)               # 这里是阈值设定
green_thresholds = ()                                   # 这里面有多个颜色的阈值
blue_thresholds = ()
yellow_thresholds = (31, 95, -8, 8, 20, 77)
# 颜色阈值的结构：(minL, maxL, minA, maxA, minB, maxB)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

while(True):
    clock.tick()
    green_led.on()
    img = sensor.snapshot()
    blobs = img.find_blobs([yellow_thresholds, red_thresholds], area_threshold=100, merge=True)
    for blob in blobs:
        x = blob[0]                 # 返回色块的x坐标
        y = blob[1]                 #          y
        width = blob[2]             #          宽度
        height = blob[3]            #          高度
        center_x = blob[5]          #           外框中心x的坐标
        center_y = blob[6]          #                  y
        color_code = blob[8]        # 返回一个16bit数字，每一个bit会对应每一个阈值（即4位十六进制）
        img.draw_rectangle([x, y, width, height])
        img.draw_cross(center_x, center_y)
        print(color_code)






