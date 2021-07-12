#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(n=10)

while(True):
    img = sensor.snapshot()

    # 获取、设置像素点
    img.get_pixel(10, 10)
    img.set_pixel(10, 10, (255,0,0))



