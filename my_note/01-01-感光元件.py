#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)       # QVGA：320*240
sensor.skip_frames(n=10)
sensor.set_auto_gain(False)             # 自动增益
sensor.set_auto_whitebal(False)         # 白平衡

# 设置窗口ROI
#sensor.set_framesize(sensor.VGA)        # 高分辨率
#sensor.set_windowing((640, 80))         # 取中间640*80的区域

# 设置翻转
# 略

while(True):
    img = sensor.snapshot()




