# Flood Fill
#
# This example shows off flood filling areas in the image.

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.QVGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()

    # seed_threshold controls the maximum allowed difference between
    # the initial pixel and any filled pixels. It's important to
    # set this such that flood fill doesn't fill the whole image.
    # seed_threshold控制初始像素和任何填充像素之间的最大允许差异。
    # 设置此项以使洪水填充不会填充整个图像非常重要。

    # floating_threshold controls the maximum allowed difference
    # between any two pixels. This can easily fill the whole image
    # with even a very low threshold.
    # floating_threshold控制任意两个像素之间允许的最大差异。这可以很容易地用一个非常低的阈值填充整个图像。

    # flood_fill will fill pixels that both thresholds.
    # flood_fill将填充这两个阈值的像素

    # You can invert what gets filled with "invert" and clear
    # everything but the filled area with "clear_background".
    # 你可以传递“invert”参数反转填充的内容，并用“clear_background”参数清除除填充区域以外的所有内容。

    x = sensor.width() // 2         # 整除，向下取整
    y = sensor.height() // 2        # 相当于从中间开始填充图像
    img = sensor.snapshot().flood_fill(x, y, \
        seed_threshold=0.08, floating_thresholds=0.08, \
        color=(255, 0, 0), invert=False, clear_background=True)

    print(clock.fps())
