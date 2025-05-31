import tkinter as tk
from tkinter import ttk

""" Combobox下拉框控件 """
"""
参数说明：
values: 选项列表，可以是列表或元组
state: "normal"表示可输入，"readonly"表示仅可选，不可输入，推荐readonly
textvarible: 绑定一个StringVar用于获取或者追踪值

函数:
current(n) 设置默认选中的第n个索引，从0开始
get() 获取当前选中项的值
set(val) 设置当前值（字符串形式）
"""
class App:
    def __init__(self, root):
        self.root=root
        
        root.after(1000,self.af)
        self.strVar = tk.StringVar()
        self.combo = ttk.Combobox(root,values=["苹果","香蕉","梨","桃子"],state="readonly",textvariable=self.strVar)
        self.combo.current(0)
        self.combo.pack(pady=20)
        
        btn = tk.Button(root,text="click",command=self.show_choice)
        btn.pack()
        
    
    def show_choice(self):
        print(f"你的选择是：{self.combo.get()}")
    def af(self):
        print(self.strVar.get())
        root.after(1000,self.af)

root = tk.Tk()
app = App(root)
root.title("Combobox组件示例")
root.geometry("300x150")

root.mainloop()