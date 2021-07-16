# Basic UART communications between OpenMV and Arduino Uno.

# 1) Wire up your OpenMV Cam to your Arduino Uno like this:
#
# OpenMV Cam Ground Pin   ----> Arduino Ground
# OpenMV Cam UART3_TX(P4) ----> Arduino Uno UART_RX(0)
# OpenMV Cam UART3_RX(P5) ----> Arduino Uno UART_TX(1)

# 2) Uncomment and upload the following sketch to Arduino:
#
# void setup() {
#   // put your setup code here, to run once:
#   Serial.begin(19200);
# }
# 
# void loop() {
#   // put your main code here, to run repeatedly:
#   if (Serial.available()) {
#     // Read the most recent byte
#     byte byteRead = Serial.read();
#     // ECHO the value that was read
#     Serial.write(byteRead);
#   }
# }

# 3) Run the following script in OpenMV IDE:

import time
from pyb import UART

# UART 3, and baudrate.                 # 其实我感觉波特率选115200会不会更好
uart = UART(3, 19200)                               # 使用给定波特率初始化
# uart.init(9600, bits=8, parity=None, stop=1)      # 使用给定参数初始化



while(True):
    uart.write("Hello World!\n")        # 将字节缓冲区写入总线，返回写入的字节数
    if (uart.any()):                    # 返回一个整数，无可用字符为0；若有可用字符则返回一个正数；若超过一个可读取字符则返回1
        print(uart.read())              # 读取字符，返回字节对象
    time.sleep_ms(1000)





