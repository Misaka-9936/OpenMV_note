# DAC Timed Write Example
#
# This example shows how to use the DAC pin output onboard your OpenMV Cam.

# 相当于可以用这个例程输出 / 读入周期信号

import math
from pyb import DAC

# create a buffer containing a sine-wave
# 创建一个包含正弦波的缓冲区
buf = bytearray(100)
for i in range(len(buf)):
    buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

# output the sine-wave at 400Hz
# 输出400Hz的正弦波
dac = DAC("P6")
dac.write_timed(buf, 400 * len(buf), mode=DAC.CIRCULAR)
