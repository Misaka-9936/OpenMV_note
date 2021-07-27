# Black Grayscale Line Following Example
#
# Making a line following robot requires a lot of effort. This example script
# shows how to do the machine vision part of the line following robot. You
# can use the output from this script to drive a differential drive robot to
# follow a line. This script just generates a single turn value that tells
# your robot to go left or right.
# 跟随机器人做一条线需要很多努力。 本示例脚本显示了如何执行跟随机器人的
# 机器视觉部分。 您可以使用此脚本的输出来驱动差分驱动机器人遵循一条线。
# 这个脚本只是产生一个转动的值，告诉你的机器人向左或向右。
#
# For this script to work properly you should point the camera at a line at a
# 45 or so degree angle. Please make sure that only the line is within the
# camera's field of view.
# 为了使这个脚本正常工作，你应该把摄像机指向45度左右的一条线。请确保只有线在相机的视野内。

import sensor, image, time, math

# Tracks a black line. Use [(128, 255)] for a tracking a white line.
# 跟踪一条黑线。使用[(128,255)]来跟踪白线。
# 注：这仅仅是L
GRAYSCALE_THRESHOLD = [(0, 64)]
#设置阈值，如果是黑线，GRAYSCALE_THRESHOLD = [(0, 64)]；
#如果是白线，GRAYSCALE_THRESHOLD = [(128，255)]

# Each roi is (x, y, w, h). The line detection algorithm will try to find the
# centroid of the largest blob in each roi. The x position of the centroids
# will then be averaged with different weights where the most weight is assigned
# to the roi near the bottom of the image and less to the next roi and so on.
# 每个roi为(x, y, w, h)，线检测算法将尝试找到每个roi中最大的blob的质心。
# 然后用不同的权重对质心的x位置求平均值，其中最大的权重分配给靠近图像底部的roi，
# 较小的权重分配给下一个roi，以此类推。
ROIS = [ # [ROI, weight]
        (0, 100, 160, 20, 0.7), # You'll need to tweak the weights for your app
        (0,  50, 160, 20, 0.3), # depending on how your robot is setup.
        (0,   0, 160, 20, 0.1)
       ]
#roi代表三个取样区域，（x,y,w,h,weight）,代表左上顶点（x,y）宽高分别为w和h的矩形，
#weight为当前矩形的权值。注意本例程采用的QQVGA图像大小为160x120，roi即把图像横分成三个矩形。
#三个矩形的阈值要根据实际情况进行调整，离机器人视野最近的矩形权值要最大，
#如上图的最下方的矩形，即(0, 100, 160, 20, 0.7)

# Compute the weight divisor (we're computing this so you don't have to make weights add to 1).
# 计算权重除数（我们计算这个，所以你不必让权重加到1）。
weight_sum = 0
for r in ROIS: 
    weight_sum += r[4] 
    # r[4] is the roi weight.
# 计算权值和。遍历上面的三个矩形，r[4]即每个矩形的权值。
# 注：相当于将他们的权重相加

# Camera setup...
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # use grayscale.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    img.draw_rectangle(ROIS[0][0], ROIS[0][1], ROIS[0][2], ROIS[0][3])
    img.draw_rectangle(ROIS[1][0], ROIS[1][1], ROIS[1][2], ROIS[1][3])
    img.draw_rectangle(ROIS[2][0], ROIS[2][1], ROIS[2][2], ROIS[2][3])

    centroid_sum = 0

    for r in ROIS:
        blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=r[0:4], merge=True) # r[0:4] is roi tuple.

        if blobs:
            # Find the blob with the most pixels.
            largest_blob = max(blobs, key=lambda b: b.pixels())
            # key是索引

            # Draw a rect around the blob.
            img.draw_rectangle(largest_blob.rect())
            img.draw_cross(largest_blob.cx(), largest_blob.cy())

            centroid_sum += largest_blob.cx() * r[4] # r[4] is the roi weight.
            # 计算centroid_sum，centroid_sum等于每个区域的最大颜色块的中心点的x坐标值乘本区域的权值

    center_pos = (centroid_sum / weight_sum) # Determine center of line.
                                                # 中间公式

    # Convert the center_pos to a deflection angle. We're using a non-linear
    # operation so that the response gets stronger the farther off the line we
    # are. Non-linear operations are good to use on the output of algorithms
    # like this to cause a response "trigger".
    # 将center_pos转换为一个偏角。我们用的是非线性运算，所以越偏离直线，响应越强。
    # 非线性操作很适合用于这样的算法的输出，以引起响应“触发器”。
    deflection_angle = 0

    # The 80 is from half the X res, the 60 is from half the Y res. The
    # equation below is just computing the angle of a triangle where the
    # opposite side of the triangle is the deviation of the center position
    # from the center and the adjacent side is half the Y res. This limits
    # the angle output to around -45 to 45. (It's not quite -45 and 45).
    # 80是X的一半，60是Y的一半。
    # 下面的等式只是计算三角形的角度，其中三角形的另一边是中心位置与中心的偏差，相邻边是Y的一半。
    # 这样会将角度输出限制在-45至45度左右。（不完全是-45至45度）。
    deflection_angle = -math.atan((center_pos-80)/60)
    #角度计算.80 60 分别为图像宽和高的一半，图像大小为QQVGA 160x120.
    #注意计算得到的是弧度值

    # Convert angle in radians to degrees.
    # 将计算结果的弧度值转化为角度值
    deflection_angle = math.degrees(deflection_angle)

    # Now you have an angle telling you how much to turn the robot by which
    # incorporates the part of the line nearest to the robot and parts of
    # the line farther away from the robot for a better prediction.
    # 现在你有一个角度来告诉你该如何转动机器人。
    # 通过该角度可以合并最靠近机器人的部分直线和远离机器人的部分直线，以实现更好的预测。
    print("Turn Angle: %f" % deflection_angle)

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
