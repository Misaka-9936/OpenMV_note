# Cartoon Filter
#
# This example shows off a simple cartoon filter on images. The cartoon
# filter works by joining similar pixel areas of an image and replacing
# the pixels in those areas with the area mean.
# 此示例显示了图像上的简单卡通滤波器。卡通化滤波通过连接图像的相似
# 像素区域并用区域平均值替换这些区域中的像素来工作。

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.QVGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()

    # seed_threshold controls the maximum area growth of a colored
    # region. Making this larger will merge more pixels.
    # seed_threshold控制着色区域的最大区域增长。 将其放大会合并更多像素。

    # floating_threshold controls the maximum pixel-to-pixel difference
    # when growing a region. Settings this very high will quickly combine
    # all pixels in the image. You should keep this small.
    # floating_threshold控制增长区域时的最大像素到像素的差异。
    # 设置高的值将快速组合图像中的所有像素。你应该使其小一些。

    # cartoon() will grow regions while both thresholds are statisfied...
    # cartoon() 将增长同时两个限制都满足的区域...

    img = sensor.snapshot().cartoon(seed_threshold=0.05, floating_thresholds=0.05)

    print(clock.fps())

# 这个函数在M4上用不了……
