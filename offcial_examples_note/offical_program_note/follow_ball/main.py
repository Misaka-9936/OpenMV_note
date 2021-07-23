threshold = (5, 70, -23, 15, -57, 0)

import sensor, image, time
from pyb import LED
import car
from pid import pid

rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

sensor.reset()
sensor.set_vflip(True)          # 打开垂直翻转模式
sensor.set_hmirror(True)        # 打开水平镜像模式
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)      # 80*60 (4,800 pixels) - O(N^2) max = 2,3040,000.
# sensor.set_windowing([0,23,80,40])
sensor.skip_frames(time = 2000)         # 如果使用QQVGA，有时会花一点时间准备帧数据

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot().binary([threshold])         # 二值化
    line = img.get_regression([100,100], robust=True)   # **线性回归**
    if line:
        rho_err = abs(line.rho()) - img.width()/2
        if line.theta() > 90:
            theta_err = line.theta() - 180
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color=127)
        print(rho_err, line.magnitude, rho_err)
        if line.magnitude() > 8:
            # if -40 < b_err < 40 and -30 < t_err < 30:
            rho_output = rho_pid.get_pid(rho_err, 1)
            theta_output = theta_pid.get_pid(theta_err, 1)
            output = rho_output + theta_output
            car.run(50+output, 50-output)
        else:
            car.run(0, 0)
    else:
        car.run(50, -50)
        pass
    # print(clock.fps())









