# Arrow Drawing
#
# This example shows off drawing arrows on the OpenMV Cam.

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.QVGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()

    img = sensor.snapshot()

    for i in range(10):
        x0 = 255
        y0 = 100
        x1 = 150
        y1 = 230
        r = 0
        g = 0
        b = 0

        # If the first argument is a scaler then this method expects
        # to see x0, y0, x1, and y1. Otherwise, it expects a (x0,y0,x1,y1) tuple.
        # 如果第一个参数是scaler，那么此方法应传递x0、y0、x1和y1。否则，它期望有一个(x0,y0,x1,y1)元组
        img.draw_arrow(x0, y0, x1, y1, color = (r, g, b), size = 30, thickness = 2)

    print(clock.fps())
