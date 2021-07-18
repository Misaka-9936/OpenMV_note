# Color Bilteral Filter Example
#
# This example shows off using the bilateral filter on color images.

import sensor, image, time

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.RGB565
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    # color_sigma controls how close color wise pixels have to be to each other to be
    # blured togheter. A smaller value means they have to be closer.
    # A larger value is less strict.
    # color_sigma控制彩色明智像素之间必须有多近的距离才能模糊。
    # 更小的值意味着它们必须更接近。
    # 较大的值不那么严格。

    # space_sigma controls how close space wise pixels have to be to each other to be
    # blured togheter. A smaller value means they have to be closer.
    # A larger value is less strict.
    # space_sigma控制空间智慧像素彼此之间必须有多近才能模糊
    # 更小的值意味着它们必须更接近。
    # 较大的值不那么严格。

    # Run the kernel on every pixel of the image.
    # 在图像的每个像素上运行核
    img.bilateral(3, color_sigma=0.1, space_sigma=1)

    # Note that the bilateral filter can introduce image defects if you set
    # color_sigma/space_sigma to aggresively. Increase the sigma values until
    # the defects go away if you see them.
    # 请注意，如果将color_sigma/space_sigma设置为聚合，双边过滤器可能会引入图像缺陷。
    # 如果你看到缺陷，增加sigma值直到缺陷消失

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
