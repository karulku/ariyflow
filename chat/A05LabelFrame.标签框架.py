import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

""" LabelFrame是一个带标题的容器控件，适合用来分组排列控件，让界面更清晰有条理 """

"""
text: 设置标签框的标题
padx/pady: 边框内边距（不是外边距）
labelanchor: 设置标题文字的位置（如n,nw,ne等）

"""

class App:
    def __init__(self, root):
        self.root = root
        self.create()
    
    def create(self):
        root.title("LabelFrame 示例")
        root.geometry("300x200")
        labelframe = tk.LabelFrame(root, text="用户信息",padx=10,pady=10)
        labelframe.pack(padx=20,pady=20,fill="both",expand=True)
        
        tk.Label(labelframe,text="姓名：").grid(row=0,column=0,sticky="w") # sticky设置对齐格式，w为左对齐
        tk.Entry(labelframe).grid(row=0,column=1,sticky="w")

        tk.Label(labelframe,text="年龄：").grid(row=1,column=0,sticky="w")
        tk.Entry(labelframe).grid(row=1,column=1,sticky="w")
root = tk.Tk()
app = App(root)
root.mainloop()