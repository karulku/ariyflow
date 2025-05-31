import tkinter as tk

"""
Scale 用于让用户通过滑动条选择一个连续范围内的数值，比如音量调节，亮度调节，进度控制等
主要参数：
from_ 滑块起始值 注意是from_不是from，因为from是python的关键字
to 滑块结束值
orient 方向，tk.HORIZONTAl或tk.VERTICAL
length 滑条长度
tickinterval 刻度间隔（显示标记）
resolution 步进大小，决定滑动的最小增量
variable 绑定的变量
command 滑动时触发的回调函数，参数是当前数值
"""

class App:
    def __init__(self,root:tk.Tk):
        self.root = root
        self.create()
    
    def create(self):
        
        self.root.geometry("400x300+400+300")
        
        scale_var = tk.IntVar(value=50)
        scale = tk.Scale(self.root,from_=10,to=70,orient=tk.HORIZONTAL,length=110,tickinterval=20,command=lambda x=scale_var.get():self.on_slide(x),resolution=0.1,variable=scale_var)
        scale.pack(pady=20)
    
    def on_slide(self,value):
        print("当前滑动值：",value)

root = tk.Tk()
app = App(root)
root.mainloop()