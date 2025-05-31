import tkinter as tk
from tkinter import ttk

"""
常用参数：
bg 背景颜色（gray lightblue lightgreen）
width/height 宽度/高度（像素）
bd 边框宽度
relief 边框样式（"sunken","raised"）
padx/pady 内边距
"""

class App:
    def __init__(self, root):
        
        self.create()
    
    def create(self):
        root.geometry("400x300+400+300")
        root.title("Frame框架的使用")
        
        top_frame = tk.Frame(root,bg="lightblue",height=50)
        top_frame.pack(fill="x")
        
        middle_frame = tk.Frame(root,bg="#3f3f3f")
        middle_frame.pack(fill="both",expand=True)
        
        bottom_frame = tk.Frame(root,bg="lightgreen",height=50)
        bottom_frame.pack(fill='x')
        
        tk.Label(middle_frame,text="这是中间区域").pack(pady=10)
        tk.Button(middle_frame,text="click").pack()
        
        middle_frame.columnconfigure(0,weight=1)
        middle_frame.rowconfigure(0,weight=1)

root = tk.Tk()
app = App(root)
root.mainloop()