# Absolute Optical Flow Rotation/Scale
# 光流绝对旋转变换示例
#
# This example shows off using your OpenMV Cam to measure
# rotation/scale by comparing the current and a previous
# image against each other. Note that only rotation/scale is
# handled - not X and Y translation in this mode.
# 此示例显示使用OpenMV Cam通过将当前图像与先前图像相互比较来测量旋转/缩放。 
# 请注意，在此模式下仅处理旋转/缩放 - 而不是X和Y平移。

# To run this demo effectively please mount your OpenMV Cam on a steady
# base and SLOWLY rotate the camera around the lens and move the camera
# forward/backwards to see the numbers change.
# I.e. Z direction changes only.
# 要有效地运行此演示，请将OpenMV安装在稳固的底座上，
# 然后 慢慢地 围绕镜头旋转摄像机，并向前/向后移动摄像机以查看数字的变化。
# 即仅改变z方向。


import sensor, image, time, math

# NOTE!!! You have to use a small power of 2 resolution when using
# find_displacement(). This is because the algorithm is powered by
# something called phase correlation which does the image comparison
# using FFTs. A non-power of 2 resolution requires padding to a power
# of 2 which reduces the usefulness of the algorithm results. Please
# use a resolution like B64X64 or B64X32 (2x faster).
# 注意！！！ 使用find_displacement()时，必须使用2的幂次方分辨率。 
# 这是因为该算法由称为相位相关的东西提供动力，该相位相关使用FFT进行图像比较。 
# 非2的幂次方分辨率要求填充到2的幂，这降低了算法结果的有用性。 
# 请使用像B64X64或B64X32这样的分辨率（快2倍）。

# Your OpenMV Cam supports power of 2 resolutions of 64x32, 64x64,
# 128x64, and 128x128. If you want a resolution of 32x32 you can create
# it by doing "img.pool(2, 2)" on a 64x64 image.
# 您的OpenMV Cam支持2的幂次方分辨率64x32,64x64,128x64和128x128。
# 如果您想要32x32的分辨率，可以通过在64x64图像上执行“img.pool（2,2）”来创建它。

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.B64X64) # Set frame size to 64x64... (or 64x32)...
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

# Take from the main frame buffer's RAM to allocate a second frame buffer.
# There's a lot more RAM in the frame buffer than in the MicroPython heap.
# However, after doing this you have a lot less RAM for some algorithms...
# So, be aware that it's a lot easier to get out of RAM issues now.
# 从主帧缓冲区的RAM中取出以分配第二帧缓冲区。
# 帧缓冲区中的RAM比MicroPython堆中的RAM多得多。
# 但是，在执行此操作后，您的某些算法的RAM会少得多......
# 所以，请注意现在摆脱RAM问题要容易得多。

# 为帧缓冲区堆栈中的图像储存分配另一个帧缓冲区，并且返回一个width、height、pixformat图像对象
extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)
# 对替换的基础图像起作用
extra_fb.replace(sensor.snapshot())

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    # This algorithm is hard to test without a perfect jig... So, here's a cheat to see it works.
    # Put in a z_rotation value below and you should see the r output be equal to that.
    # 如果没有完美的夹具，这个算法很难测试......所以，这是一个让它看起来有效的骗子...
    # 在下面输入一个z_rotation值，你应该看到r的输出等于它。
    if(0):
        expected_rotation = 20.0
        img.rotation_corr(z_rotation=expected_rotation)

    # This algorithm is hard to test without a perfect jig... So, here's a cheat to see it works.
    # Put in a zoom value below and you should see the z output be equal to that.
    if(0):
        expected_zoom = 0.8
        img.rotation_corr(zoom=expected_zoom)

    # For this example we never update the old image to measure absolute change.
    # 对于此示例，我们从不更新旧图像以测量绝对变化。
    displacement = extra_fb.find_displacement(img, logpolar=True)

    # Offset results are noisy without filtering so we drop some accuracy.
    # 没有滤波，偏移结果是嘈杂的，所以我们降低了一些精度。
    rotation_change = int(math.degrees(displacement.rotation()) * 5) / 5.0
    zoom_amount = displacement.scale()

    if(displacement.response() > 0.1): # Below 0.1 or so (YMMV) and the results are just noise.
                                        # 低于0.1左右（YMMV），结果只是噪音。
        print("{0:+f}r {1:+f}z {2} {3} FPS".format(rotation_change, zoom_amount, \
              displacement.response(),
              clock.fps()))
    else:
        print(clock.fps())
