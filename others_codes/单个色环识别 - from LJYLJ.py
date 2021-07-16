# 本算法用到了腐蚀膨胀、深度分割、二级化滤波、阈值分割算法

import sensor, image, time, pyb
import lcd, math
import ujson, json
from pyb import UART
from pyb import LED

obj = [[12,0], [10,12], [22,10], [99,11]]       # json
                                                # 固定写好，可以不用改

threshold_index = 0         # 0 for red, 1 for green, 2 for blue
                            # 相当于是数组，对应下面的红色阈值

objthresholds = [(51, 76, 8, 77, 7, 23),        # generic_red_thresholds
                (37, 60, -32, 33, 0, 67),       # generic_green_thresholds
                (37, 60, -5, 33, -60, 67)]      # generic_blue_thresholds

greythreshold = [(100, 255)]

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
# 色环识别白平衡默认开启

uart = UART(3, 115200)

red_led.off()
green_led.off()
blue_led.off()

# 做差比较色块的大小
def compareBlob(blob1, blob2):
    tmp = blob1.pixels() - blob2.pixels()
    if tmp == 0:
        return 0
    elif tmp > 0:
        return 1
    else:
        return -1

flag_color = 1

while(True):
    img = sensor.snapshot()
    img.lens_corr(1.0)                  # 镜头畸变矫正
                                        # accepet
    if(urat.any()):                     # 如果串口接收到任何数据，则：
        time.sleep(200)                 # 延时（缓冲）
        d = uart.read()                 # 将数据读给d
        da = str(d, "utf-8")            # 这个可以不需要

        jsobj = ujson.loads(da)
        for key in jsobj.keys():
            print('key:%s value:%s' % (key,jsobj.get(key)))
            if(jsobj.get("RGB")=="R"):
                flag_color = 1
            elif(jsobj.get("RGB")=="G"):
                flag_color = 2
            elif(jsobj.get("RGB")=="B"):
                flag_color = 3
            else:
                flag_color = 0

    if(flag_color == 1):
        img.binary([objthresholds[0]])          # 阈值分割（红色），进行二值化
        img.dilate(2)                           # 进行腐蚀膨胀算法

        blobs = img.find_blobs(greythreshold, pixels_threshold=2025, area_threshold=1600, merge=True)
        if len(blobs) == 0:
            continue
        bigBlob = blob[0]
        for blob in blobs:
            if compareBlob(Blgblob, blob) == -1:
                bigBlob = blob
            img.draw_rectangle(bigBlob.rect())
            print(bigBlob.cx(), bigBlob.cy())
            output_str = json.dumps([bigBlob.cx(), bigBlob.cy()])
            data_out = "{\"R\":" + output_str + "}\r\n"
        red_led.on()
        green_led.off()
        blue_led.off()
        uart.write(data_out)
        print(data_out)

    if(flag_color == 2):
        img.binary([objthresholds[1]])
        img.dilate(4)

        blobs = img.find_blobs(greythreshold, pixels_threshold=2025, area_threshold=1600, merge=True)
        if len(blobs) == 0:
            continue
        bigBlob = blob[0]
        for blob in blobs:
            if compareBlob(Blgblob, blob) == -1:
                bigBlob = blob
            img.draw_rectangle(bigBlob.rect())
            print(bigBlob.cx(), bigBlob.cy())
            output_str = json.dumps([bigBlob.cx(), bigBlob.cy()])
            data_out = "{\"G\":" + output_str + "}\r\n"
        red_led.off()
        green_led.on()
        blue_led.off()
        uart.write(data_out)
        print(data_out)

    if(flag_color == 3):
        img.binary([objthresholds[2]])
        img.dilate(4)

        blobs = img.find_blobs(greythreshold, pixels_threshold=2025, area_threshold=1600, merge=True)
        if len(blobs) == 0:
            continue
        bigBlob = blob[0]
        for blob in blobs:
            if compareBlob(Blgblob, blob) == -1:
                bigBlob = blob
            img.draw_rectangle(bigBlob.rect())
            print(bigBlob.cx(), bigBlob.cy())
            output_str = json.dumps([bigBlob.cx(), bigBlob.cy()])
            data_out = "{\"B\":" + output_str + "}\r\n"
        red_led.off()
        green_led.off()
        blue_led.on()
        uart.write(data_out)
        print(data_out)




























