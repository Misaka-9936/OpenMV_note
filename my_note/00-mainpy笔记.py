# main.py -- put your code here!

import sensor, image, time

# sensor引入感光元件的模块
# 设置摄像头

sensor.reset()                          # 重置并初始化感光元件
sensor.set_pixformat(sensor.RGB565)     # Set pixel format to RGB565 (or GRAYSCALE)
                                        # RGB565彩色，GRAYSCALE灰度
sensor.set_framesize(sensor.QVGA)       # Set frame size to QVGA (320x240) 设置图像的大小
                                        # QQVGA: 160x120,QVGA: 320x240,VGA: 640x480
                                        # VGA彩色为压缩格式，不支持图像算法。
                                        # MT9V034快门摄像头仅灰度
sensor.skip_frames(time = 2000)         # Wait for settings take effect.
                                        # 跳过n张照片，在更改设置后，跳过一些帧，等待感光元件变稳定。
clock = time.clock()                    # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
                                    # 拍摄一张照片，img为一个image对象
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.

