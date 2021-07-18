# A————>B，侧面摄像头
# 绕杆：摄像头一直盯着绕
# 飞控部分把拿到的坐标映射到yaw和roll作为期望角度，实现平移的同时旋转

# 下面是绕易拉罐的方法：

import sensor, image, time
import math
import pyb
from pyb import UART, LED, Pin

blue_threshold = (10, 33, -6, 19, -36, -3)
green_threshold = (52, 82, 50, 84, -3, 65)
tiao_threshold = (61, 99, -40, 0, 18, 50)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(500)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

clock = time.clock()

# 状态机
class STATE():
    pass


# ......



# 串口初始化
uart = UART(3, 115200)
uart.init(115200, bit=8, parity=None, stop=1, timeout_char=1000)
def uart_read(timer):
    pass

# ......


# 杆太细，距离太远，即使跳一个像素，对距离的影响也高达20cm

# 使用VGA画幅，但裁剪为很宽的矩形，这样识别杆的误差波动会小很多"



