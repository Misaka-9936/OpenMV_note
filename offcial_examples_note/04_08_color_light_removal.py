# Color Light Removal
# This example shows off how to remove bright lights from the image.
# You can do this using the binary() method with the "zero=" argument.
# 彩图光线去除例程
# 此示例显示如何从图像中删除明亮的灯光。
# 您可以使用带有“zero =”参数的binary()方法执行此操作。
#
# Removing bright lights from the image allows you to now use
# histeq() on the image without outliers from oversaturated
# parts of the image breaking the algorithm...
# 从图像中删除明亮的光线允许您在图像上使用histeq()，
# 而不会使图像的过饱和部分的异常值破坏算法...

import sensor, image, time

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

thresholds = (90, 100, -128, 127, -128, 127)
# 显然你需要自己调试这个阈值，我老调参了

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot().binary([thresholds], invert=False, zero=True)

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
