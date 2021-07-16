# Adaptive Histogram Equalization
#
# This example shows off how to use adaptive histogram equalization to improve
# the contrast in the image. Adaptive histogram equalization splits the image
# into regions and then equalizes the histogram in those regions to improve
# the image contrast versus a global histogram equalization. Additionally,
# you may specify a clip limit to prevent the contrast from going wild.

# 此示例展示了如何使用自适应直方图均衡来改善图像中的对比度。 
# 自适应直方图均衡将图像分割成区域，然后均衡这些区域中的直方图，
# 以改善图像对比度与全局直方图均衡化。 
# 此外，您可以指定剪辑限制以防止对比度变得狂野。

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()

    # A clip_limit of < 0 gives you normal adaptive histogram equalization
    # which may result in huge amounts of contrast noise...
    # clip_limit <0为您提供正常的自适应直方图均衡，这可能会导致大量的对比噪音...

    # A clip_limit of 1 does nothing. For best results go slightly higher
    # than 1 like below. The higher you go the closer you get back to
    # standard adaptive histogram equalization with huge contrast swings.
    # clip_limit=1 什么都不做。为获得最佳效果，请略高于1，如下所示。 
    # 越高，越接近标准自适应直方图均衡，并产生巨大的对比度波动。

    img = sensor.snapshot().histeq(adaptive=True, clip_limit=3)

    print(clock.fps())
