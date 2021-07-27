# Image Histogram Info Example
# 图像直方图信息示例
#
# This script computes the histogram of the image and prints it out.
# 该脚本计算图像的直方图并将其打印出来。

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) # or RGB565.
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Gets the grayscale histogram for the image into 8 bins.
    # Bins defaults to 256 and may be between 2 and 256.
    # 获取图像的灰度直方图为8个bin。
    # Bins默认为256，可能在2到256之间。
    print(img.get_histogram(bins=8))
    print(clock.fps())

# You can also pass get_histogram() an "roi=" to get just the histogram of that area.
# get_histogram() allows you to quickly determine the color channel information of
# any any area in the image.
# 你也可以通过传递一个“roi =”给get_histogram（）来得到该区域的直方图。
# get_histogram（）允许您快速确定图像中任何区域的颜色通道信息。
