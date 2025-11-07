import serial
import time
from threading import Thread, Event, Lock
import os
import random

# 生成数据
data1 = [b"\xaa\x55"+os.urandom(8) for i in range(8)]
data2 = [os.urandom(10) for _ in range(8)]
data = data1+data2
random.shuffle(data)

# 串口定义和计数
ser = serial.Serial(port="COM5", baudrate=9600, timeout=0.5)
global cnt
cnt = 0
mut = Lock()

# 监听串口传来的数据
def listener():
    global cnt
    recv_cnt = 0
    while is_run.is_set():
        reading = ser.read(10)
        if reading:
            
            mut.acquire()
            cnt-=1
            mut.release()
            recv_cnt+=1
            
            print(f"接收：{reading.hex()} 当前接收次数：{recv_cnt}")
    

if __name__ == "__main__":

    is_run = Event()
    is_run.set()
    t = Thread(target=listener)
    t.start()
    
    send_cnt = 0
    for i in range(len(data)):
        ser.write(data[i])
        
        mut.acquire()
        cnt+=1
        mut.release()
        send_cnt+=1
        
        print(f"发送：{data[i].hex()} 当前发送次数：{send_cnt}")
        
        time.sleep(0.1)
    if cnt == 0:
        is_run.clear()
    else:
        time.sleep(3)
        is_run.clear()
    
    print(f"有{cnt}个数据包发送后没有被接收！")
    t.join()