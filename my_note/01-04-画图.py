#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    img = img.draw_rectangle((20,30,41,51), color=(255,255,255))





