# DAC Control Example
#
# This example shows how to use the DAC pin output onboard your OpenMV Cam.

import time
from pyb import DAC

dac = DAC("P6") # Must always be "P6".

while(True):
    # The DAC has 8-12 bits of resolution (default 8-bits).
    for i in range(256):
        dac.write(i)            # DAC输出，范围用万用表测量大概在-0.015——0.013V
        print(i)                # 电压变化范围太小，我暂时不知道有什么用
        time.sleep_ms(1000)
    for i in range(256):
        dac.write(255-i)
        print(i)
        time.sleep_ms(1000)
