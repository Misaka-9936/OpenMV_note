#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor, img, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)

ROI = (80, 30, 15, 15)

while(True):
    img = sensor.snapshot()
    img.get_statistics(roi=ROI)         # 注意：roi、bin等参数，一定要显式的标明
    # 剩下的众数等略






