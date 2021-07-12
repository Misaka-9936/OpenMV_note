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

ROI = (80, 30, 15, 15)

while(True):
    clock.tick()                                    # 开始追踪运行时间
    img = sensor.snapshot()
    statistics = img.get_statistics(roi=ROI)
    color_l = statistics.l_mode()                   # LAB是一种色彩模式，三个通道分别为L（亮度）、A（红绿）、B（蓝黄），区别于RGB的三个通道
    color_a = statistics.a_mode()
    color_b = statistics.b_mode()
    print(color_l, color_a, color_b)
    img.draw_rectangle(ROI)                         # 此函数能在图像上绘制一个矩形






