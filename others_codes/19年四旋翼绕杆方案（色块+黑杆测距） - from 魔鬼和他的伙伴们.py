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
black_threshold = (7, 31, -22, 13, -18, 18)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(500)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

clock = time.clock()

# 状态机
class STATE():
    state_machine = 0
    point = 0           # 定点，利用坐标或者光流
    set_out = 1         # 出发，从定点起步前飞
    line = 2            # 直线巡线，光流控制向前速度，坐标调节y轴
    turn_left = 3       # 保持巡线左转
    turn_right = 4      # 保持巡线右转
    l_right_angle = 5   # 左转90
    r_right_angle = 6   # 右转90
    land = 7            # 降落
    height_rise = 8     # 高度上升
    height_drop = 9     # 高度下降

    # 添加测试用
    right_line = 10     # 有线加速右飘
    right_b = 11        # 向后偏置右飘
    right = 12          # 无偏置右飘
    left_line = 13      # 有线左飘
    left_b = 14         # 向后偏置左飘
    right_bottom = 15   # 底线右飘，利用底线坐标

# 状态机初始化
state = STATE()

# 所有的数据变量
# 流程：
step = 0        # 暂时定义为0起飞，1巡线判断，2最后的定点降落判断稳定，
                # 3一直发送降落命令，4巡线。后面需要什么流程就加什么……
# 命令
cmd = 1
# 高度
height = 100

class DATA():
    # 色块
    blob_x = 80
    blob_y = 60
    length = 200

    # 准备好发送的信息
    send_x = 80
    send_y = 60
    send_angle = 0

    # 16个发送数据
    send_buf = [0x00] * 16

# 数据位初始化
data = DATA()
data.send_buf[0] = 0x13
data.send_buf[1] = 0x14

# 常量
class CONST():
    # 用来判断是否到达正常高度，根据定高适当修改
    target_height = 80
    # roi
    roi_all = [0, 0, 160, 120]
    # 面积和距离的比例
    k = 400

# 常量初始化
const = CONST()

# 标志位
class FLAG():
    # 0无 1有 2异常
    circle = 0      # 圆
    line_f = 0      # 前
    line_m = 0      # 中
    line_l = 0      # 左
    line_r = 0      # 右
    line_b = 0      # 后
    line = 0        # 线
    led = 0         # led灯
    timer = 0       # 定时器计时

    usb = 0         # 1左2右

    cont2 = 0
    cont = 0
    ll = 0
    rr = 0
    circle_cont = 0

    off = 1

# 定时
timer_10ms = 0
timer_1s = 0

# 标志位初始化
flag = FLAG()

# 串口初始化
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000)
def uart_read(timer):
    global timer_10ms
    global timer_1s
    global step
    global cmd
    global height

    if flag.timer == 1:
        timer_10ms = timer_10ms + 1
        timer_1s = timer_10ms // 100
    else:
        timer_10ms = 0
        timer_1s = 0

    if uart.any():
        m_1 = uart.readchar()
        if m_1 == 0x05:
            m_2 = uart.readchar()
            if m_2 == 0x20:
                cmd = uart.readchar()
                height = uart.readchar()
                m_5 = uart.readchar()
                m_6 = uart.readchar()
                if cmd == 0:
                    step = 0

def uart_send():
    for i in range(16):
        uart.writechar(data.send_buf[i])

tim = pyb.Timer(4, freq=100)
tim.callback(uart_read)

def color_blob(threshold):
    blobs = img.find_blobs([threshold], x_stride=3, y_stride=3, area_threshold=50)
    if len(blobs) > 0:
        area = 0
        largest_blob = blob[0]
        largest_area = 0
        count_flag = 0
        for blob in blobs:
            area = blob.area()
            if area >= largest_area:
                largest_blob = blob
                largest_area = largest_blob.area()
        # Draw a rect around the blob
        img.draw_rectangle(largest_blob.rect())
        cx = largest_blob.cx()
        cy = largest_blob.cy()
        img.draw_cross(cx, cy)
        Lm = largest_blob.w()
                                        # 杆太细，距离太远，即使跳一个像素，对距离的影响也高达10cm
                                        # 高度不会变以后，用宽度为参考
                                        # 但4cm的跳动仍不可接受
                                        # 使用VGA画幅，但裁剪为很宽的矩形，这样识别杆的误差波动会小很多
                                        # 1cm的波动是可以容忍的，飞机能够正常飞行
        length = const.k / Lm
        return int(length), cx, cy
    return 200, 80, 60

while(True):
    clock.tick()
    img = sensor.snapshot()
    data.length = 200
    data.blob_x = 80
    data.blob_y = 60
    # if (cmd == 1) and (height >= const.target_height):
    data.length, data.blob_x, data.blob_y = color_blob(red_threshold)

    print(data.length, data.blob_x, data.blob_y)

    data.send_buf[2] = state.state_machine
    data.send_buf[3] = data.blob_x
    data.send_buf[4] = data.blob_y
    data.send_buf[5] = data.length

    uart_send()

    pyb.LED(2).toggle()


