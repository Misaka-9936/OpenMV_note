# Untitled - By: Du - 周日 7月 11 2021

# 最基本的四行代码：
import sensor, image, time, pyb             # 引入最基本的库
import math
from pyb import UART                        # 开启串口通信
from pyb import LED                         # 开启LED，在脱机状态下可以看到程序进行到了哪一步

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

p = pyb.Pin("P0", pyb.Pin.IN)               # 给OpenMV一个高、低电平来判断是否可以识别色块

global left, middle, right, VAL             # 声明数个全局变量
global color
global flag_color                           # 标志变量
                                            # 用它判定这些while循环进行到哪一步

left = 0            # 赋初值
middle = 0
right = 0

flag_color = 0      ##########################flag_color选择值##########################
                                                # 到时候在现场调试阈值
red_threshold = (58, 40, 77, -46, 72, 28)       # 红色颜色阈值
green_threshold = (39, 93, -71, -28, -22, 67)   # 绿色颜色阈值
blue_threshold = (30, 59, 101, -53, -71, -21)   # 蓝色颜色阈值

# 程序的核心部分：
red_color_code = 1          # code = 2^0 = 1 = 0001H
green_color_code = 2        # code = 2^1 = 2 = 0010H
blue_color_code = 4         # code = 2^2 = 4 = 0100H
black_color_code = 8        # code = 2^3 = 8 = 1000H
                            # 红色、绿色、蓝色和没有识别到的，对应着2的幂次

# 摄像头sensor最基本的初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)       # 160 * 120
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)

clock = time.clock()

# 打开一个串口（声明一个串口通信）
# uart.init(115200, bits=8, parity=None, stop=1)
uart = UART(3, 115200)      # 波特率是115200，常用的波特率有115200和9600


# lcd.init()                # 液晶显示屏init


#LED(4).on()                # 当光线弱时，用于补光，这是xx科技的OpenMV
# 星瞳科技的用这个，三个LED都打开就是白光
def Light():                # 但效果不好，不如直接外界补光
    red_led.on()
    green_led.on()
    blue_led.on()


# 下面就是主程序了：
while(flag_color == 0):     # flag_color的默认值为0
    VAL = p.value()         # 读取P0值（P0在上面定义过了）
    blue_led.on()           # 蓝色的LED打开
    print(VAL)              # 输出这个值

                            # 如果主控从P0口给了OpenMV的P0口一个低电平的话，标志位置1
    if VAL == 0:            # 检测到高电平后（低？？？）
        flag_color = 1      # 颜色检测标志位后：置1

    if flag_color == 1:     # 若标志位为1，则关闭蓝色LED，跳出循环
        blue_led.off()
        break

while(flag_color == 1):     # flag_color为1
    colok.tick()            # 开始计频
    img = sensor.snapshot() # OpenMV捕获一帧图像
    img.draw_rectangle((5,55,50,73), color=(0x00,0x00,0x00))
    img.draw_rectangle((105,55,50,73), color=(0x00,0x00,0x00))
    img.draw_rectangle((205,55,50,73), color=(0x00,0x00,0x00))
    # 三个识别区的位置（根据储物位置和摄像头位置调整）

    # 下面就是算法了：
    # 这里调用了色块库blob，并且将red、green、blue三种颜色的blob合并
    blob_left = img.find_blobs([red_threshold,green_threshold,blue_threshold], area_threshold=200, merge=True, roi=(5,55,50,73))
    blob_middle = img.find_blobs([red_threshold,green_threshold,blue_threshold], area_threshold=200, merge=True, roi=(105,55,50,73))
    blob_right = img.find_blobs([red_threshold,green_threshold,blue_threshold], area_threshold=200, merge=True, roi=(205,55,50,73))

    left = 0
    middle = 0
    right = 0

    #####################################判断左边物块的颜色#########################################
    if blob_left:
        for blob in blob_left:              
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            center_x = blob[5]
            center_y = blob[6]
            color_code = blob[8]
        # 添加颜色说明
            if color_code == red_color_code:
                img.draw_string(x, y-10, "red", color=(0xFF,0x00,0x00))
                left = 1
            elif color_code == green_color_code:
                img.draw_string(x, y-10, "green", color=(0x00,0xFF,0x00))
                left = 2
            elif color_code == blue_color_code:
                img.draw_string(x, y-10, "blue", color=(0x00,0x00,0xFF))
                left = 3
            color = color_code
            img.draw_rectangle([x, y, width, height])
            img.draw_cross(center_x, center_y)
            # print("%d" % left)
            # uart.write("%d" % left)     # 串口通信

    ######################################中间颜色检测#############################################
    if blob_middle:
        for blob in blob_middle:
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            center_x = blob[5]
            center_y = blob[6]
            color_code = blob[8]
        # 添加颜色说明
            if color_code == red_color_code:
                img.draw_string(x, y-10, "red", color=(0xFF,0x00,0x00))
                left = 1
            elif color_code == green_color_code:
                img.draw_string(x, y-10, "green", color=(0x00,0xFF,0x00))
                left = 2
            elif color_code == blue_color_code:
                img.draw_string(x, y-10, "blue", color=(0x00,0x00,0xFF))
                left = 3
            color = color_code
            # length = 6943 * math.sin(0.0001625*height+3.089)
            img.draw_rectangle([x, y, width, height])
            img.draw_cross(center_x, center_y)
            # print(length)
            # print("%d" % middle)
            # uart.write("%d" % middle)     # 串口通信

    #####################################右侧物块颜色检测###########################################
    if blob_right:
        for blob in blob_right:
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            center_x = blob[5]
            center_y = blob[6]
            color_code = blob[8]
        # 添加颜色说明
            if color_code == red_color_code:
                img.draw_string(x, y-10, "red", color=(0xFF,0x00,0x00))
                left = 1
            elif color_code == green_color_code:
                img.draw_string(x, y-10, "green", color=(0x00,0xFF,0x00))
                left = 2
            elif color_code == blue_color_code:
                img.draw_string(x, y-10, "blue", color=(0x00,0x00,0xFF))
                left = 3
            color = color_code
            img.draw_rectangle([x, y, width, height])
            img.draw_cross(center_x, center_y)
            # print("%d" % right)
            # uart.write("%d" % right)     # 串口通信
            # time.sleep(10)
    ####################################将检测到的颜色发送###########################################

    ######################################颜色检测与串口#############################################   
            # elif color_code == 4:
                # print("blue")
                # command = "b"
                # uart.write(command)
                # time.sleep(10)
    # print("%d" % left)
    # print("%d" % middle)
    # print("%d" % right)
        if left != 0 and right != 0 and middle != 0 and left != right and right != middle:      # 预防出现偏差的情况
            if left == 1 and middle == 2 and right == 3:            # 对应着6种情况，6种符号
                print("%d%d%d" % (left, middle, right))
                # uart.write("%d%d%d" % (left, middle, right))      # 数字，改串口直接改这里
                uart.write('z')                                     # 字符
            if left == 1 and middle == 3 and right == 2:
                print("%d%d%d" % (left, middle, right))
                # uart.write("%d%d%d" % (left, middle, right))
                uart.write('x')
            if left == 2 and middle == 1 and right == 3:
                print("%d%d%d" % (left, middle, right))
                # uart.write("%d%d%d" % (left, middle, right))
                uart.write('c')
            if left == 2 and middle == 3 and right == 1:
                print("%d%d%d" % (left, middle, right))
                # uart.write("%d%d%d" % (left, middle, right))
                uart.write('v')
            if left == 3 and middle == 1 and right == 2:
                print("%d%d%d" % (left, middle, right))
                # uart.write("%d%d%d" % (left, middle, right))
                uart.write('b')
            if left == 3 and middle == 2 and right == 1:
                print("%d%d%d" % (left, middle, right))
                # uart.write("%d%d%d" % (left, middle, right))
                uart.write('n')
        if uart.any():                  # 判断是否跳出当前循环（flag_color=1是循环）
            tmp_data = uart.readline()
            red_led.on()
            print(tmp_data)
            if tmp_data == b'0':        # 检测物块颜色是否被接受（作者那里arduino通信出了点问题，就加了b）
                flag_color = 2
                red_led.off()
                break                   # 已被接受，此函数结束

######################################二维码扫描与串口#############################################
while(flag_color == 2):
    clock.tick()
    # Light()                           # 要外界补光，不要用自带的灯
    img0 = sensor.snapshot()            # 新的图片不能和前面img相同
    img0.lens_corr(1.8)                 # 要用新版的OpenMV，旧版没有这个函数
    for QR in img0.find_qrcodes():      # 扫码不清楚的话，可以用扫码枪，不过那都是后话了
        code = QR.payload()             
        img0.draw_rectangle(QR.rect(), color=(255,48,48))
        if code == '123':
            uart.write('z')             # 串口终端显示
            print('123')
            red_led.on()
            red_led.off()
            flag_color = 3
            break
        elif code == '132':
            uart.write('x')
            red_led.on()
            red_led.off()
            print('132')
            flag_color = 3
            break
        elif code == '213':
            uart.write('c')
            red_led.on()
            red_led.off()
            print('213')
            flag_color = 3
            break
        elif code == '231':
            uart.write('v')
            red_led.on()
            red_led.off()
            print('231')
            flag_color = 3
            break
        elif code == '312':
            uart.write('b')
            red_led.on()
            red_led.off()
            print('312')
            flag_color = 3
            break
        elif code == '321':
            uart.write('n')
            red_led.on()
            red_led.off()
            print('321')
            flag_color = 3
            break

#########################################完成任务之后##############################################
while(flag_color == 3):                 # 此时标志位为3，代表上面的所有程序已经执行完毕
    green_led.on()                      # 亮起绿光提示

