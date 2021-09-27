import serial
import serial.tools.list_ports
import time
import random
from playsound import playsound

class Communication():
    #初始化
    def __init__(self,com,bps,timeout):
        self.port = com
        self.bps = bps
        self.timeout =timeout
        global Ret
        try:
            # 打开串口，并得到串口对象
             self.main_engine = serial.Serial(self.port,self.bps,8,stopbits=1,timeout=self.timeout)
            # 判断是否打开成功
             if (self.main_engine.is_open):
               Ret = True
        except Exception as e:
            print("---异常---：", e)

    #打开串口
    def Open_Engine(self):
        self.main_engine.open()

    #关闭串口
    def Close_Engine(self):
        self.main_engine.close()
        print(self.main_engine.is_open)  # 检验串口是否打开

    #发数据
    def Send_data(self,data):
        self.main_engine.write(data)

#出拳
def punch():
    #######################
    # 机器随机出拳
    i = random.randint(1, 3)
    if i == 1:
        Control.Send_data(ShiTou)
    elif i == 2:
        Control.Send_data(Bu)
    else:
        Control.Send_data(JianDao)
    return i #返回出拳

def start_hand():
    for i in range(2):
        Control.Send_data(Bu)
        time.sleep(0.5)
        Control.Send_data(Reset)
        time.sleep(0.5)

def reset():
    Control.Send_data(Reset)

Ret = True  # 是否创建成功标志
Control = Communication("com3", 9600, 0.5)
ShiTou = bytes.fromhex('55 55 17 03 06 0A 00 01 D0 07 02 84 03 03 84 03 04 84 03 05 84 03 06 DC 05')
JianDao = bytes.fromhex('55 55 17 03 06 0A 00 01 D0 07 02 D0 07 03 D0 07 04 84 03 05 84 03 06 DC 05')
Bu = bytes.fromhex('55 55 17 03 06 0A 00 01 84 03 02 D0 07 03 D0 07 04 D0 07 05 D0 07 06 DC 05')
Reset = bytes.fromhex('55 55 17 03 06 0A 00 01 40 06 02 14 05 03 E2 04 04 14 05 05 14 05 06 DC 05')
# Control.Send_data(JianDao)
# time.sleep(2)
# reset()
# time.sleep(1)