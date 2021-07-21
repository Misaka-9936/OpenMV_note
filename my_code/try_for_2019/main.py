#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor, image, time
import pyb
import math
from pyb import LED
from pyb import UART

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

# 将P0脚设置为接受第一个控制命令的引脚
p = pyb.Pin("P0", pyb.Pin.IN)

global VAL
global code_step
global color_code
global K

VAL = 1
code_step = 0
K = 1410

yellow_threshold = (97, 98, -16, -13, 70, 94)
# test_yellow_threshold = (76, 95, -22, 5, 0, 42)
black_threshold = (3, 24, -24, -2, -5, 21)

yellow_color_code = 1
test_yellow_color_code = 2

uart = UART(3, 115200)          # 初始化串口，波特率115200

# 识别杆的时候再启动
# sensor.reset()
# sensor.set_pixformat(sensor.RGB565)
# sensor.set_framesize(sensor.VGA)
# sensor.skip_frames(time = 2000)
# sensor.set_auto_gain(False)
# sensor.set_auto_whitebal(False)

clock = time.clock()

########################################## code_step == 0，待机，等待控制指令 ##########################################
while(code_step == 0):
    # clock.tick()
    red_led.on()
    VAL = p.value()             # 获取引脚返回值的数字逻辑级别
    print("VAL = ", VAL)
                                # 获取到引脚低电平后，跳出等待循环
    if VAL == 0:                # 注意：VAL悬空时是1
        code_step = 1
    print("code_step = ", code_step)

    if code_step == 1:
        red_led.off()
        print("has broke")
        break

    # 测试用
    code_step = 1
    red_led.off()
    break

########################################## code_step == 1，识别竖杆、测距 ##########################################
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing(640, 100)
sensor.skip_frames(time = 500)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

while(code_step == 1):
    clock.tick()                # 开始计频
    blue_led.on()

    img = sensor.snapshot()
    blobs = img.find_blobs([black_threshold], area_threshold=400, merge=True)
    for blob in blobs:
        if len(blobs) > 0:
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            cx = blob[5]
            cy = blob[6]
            img.draw_rectangle([x, y, width, height])           # rect
            img.draw_cross(cx, cy)
            Lm = width
            length = K/Lm
            print("length =", length, "width =", width, "FPS =", clock.fps())
    # K = 物体放置的距离 * 打印出的物体像素大小
    # K = 30cm * 49(width) = 1470

    # 测试用
    code_step = 2
    blue_led.off()
    break

########################################## code_step == 2，识别黄色色块和条形码 ##########################################
# 官方给出的是RGB颜色，我们需要转换为LAB

# 重新重启摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 500)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

while(code_step == 2):
    clock.tick()
    green_led.on()
    img = sensor.snapshot()

    # 标识出色块识别区域位置
    img.draw_rectangle(120, 0, 80, 240, color=(255,255,255))

    # 色块识别
    blob_yellow = img.find_blobs([yellow_threshold], area_threshold=100, merge=True, roi=(120,0,80,240))
    # 这里后面要调以下ROI，看看哪种方式最好，如果飞机水平足够，就把横着拉满

    if blob_yellow:
        for blob in blob_yellow:
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            cx = blob[5]
            cy = blob[6]
            color_code = blob[8]            # 返回一个32位二进制数字

        img.draw_rectangle([x, y, width, height])
        img.draw_cross(cx, cy)
        print("color_code =", color_code, "FPS =", clock.fps())

        # 给飞控发送标识符

        # 问：识别黄色条形码，到底是识别barcode，还是识别黄色？抑或是两者同时满足才算是识别到？
        # 答：先分别测试看看效果

    # 测试用
    code_step = 3
    green_led.off()
    break

########################################## code_step == 3，识别二维码 ##########################################
while(code_step == 3):
    clock.tick()
    red_led.on()
    sensor.set_windowing((350,200))
    img0 = sensor.snapshot()

    img0.lens_corr(1.5)         # 官方推荐参数为1.8
    qrcodes = img0.find_qrcodes()
    for QR in qrcodes:
        code = QR.payload()        # 返回QR的有效载荷
        img0.draw_rectangle(QR.rect(), color=(255,255,255))
        print("code =", code, "FPS =", clock.fps())

    # 测试用
    # code_step = 4
    # red_led.off()
    # break

# 注：如果是QVGA，识别5cm的二维码最大范围只有15cm左右
#     如果用VGA，最大范围就有30cm左右，但相应的，代价就是只有7帧
# 注：经测试，VGA情况下裁剪窗口大小，使帧率有了显著的提升（24帧），但二维码识别效果变差……
#     200 * 200 测试不行，但300 * 200 测试可以，效果很好
# 注：二维码/镜头一定要对正，否则识别的成功率会中幅下降
# 注：若二维码上有遮挡，甚至有阴影，也会在相当程度上影响到识别效果
# 注：二维码有黑色边框也会干扰到识别效果

########################################## code_step == 4，待机等待飞行结束 ##########################################
while(code_step == 4):
    clock.tick()
    green_led.on()





























