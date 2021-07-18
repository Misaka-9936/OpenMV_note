# Color Binary Filter Example
# 颜色二值化滤波例子
#
# This script shows off the binary image filter. You may pass binary any
# number of thresholds to segment the image by.
# 这个脚本展示了二值图像滤波。
# 您可以传递二进制任意的阈值来分割图像。

import sensor, image, time

sensor.reset()
sensor.set_framesize(sensor.QVGA)
sensor.set_pixformat(sensor.RGB565)
sensor.skip_frames(time = 2000)
clock = time.clock()

# Use the Tools -> Machine Vision -> Threshold Edtor to pick better thresholds.
# 设置颜色阈值，如果是rgb图像，六个数字分别为(minL, maxL, minA, maxA, minB, maxB)；
# 如果是灰度图，则只需设置（min, max）两个数字即可。
red_threshold = (0,100,   0,127,   0,127) # L A B
green_threshold = (0,100,   -128,0,   0,127) # L A B
blue_threshold = (0,100,   -128,127,   -128,0) # L A B

while(True):

    # Test red threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([red_threshold])
        print(clock.fps())
        #image.binary(thresholds, invert=False)此函数将在thresholds内的
        #图像部分的全部像素变为1白，将在阈值外的部分全部像素变为0黑。invert将图像
        #的0 1（黑 白）进行反转，默认为false不反转。
    
    # Test green threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([green_threshold])
        print(clock.fps())

    # Test blue threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([blue_threshold])
        print(clock.fps())

    # Test not red threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([red_threshold], invert = 1)
        print(clock.fps())

    # Test not green threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([green_threshold], invert = 1)
        print(clock.fps())

    # Test not blue threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([blue_threshold], invert = 1)
        print(clock.fps())
