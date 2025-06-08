import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

"""
Menu是一个可以添加在窗口顶部的菜单栏

add_cascade(label=...,menu=...) 添加子菜单
add_command(label="",command=...) 添加菜单项
add_separator() 添加分割线
tearoff=0 去除虚线撕扣 ###记得加上！！！###

"""

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.create()
    
    def create(self):
        self.menu_bar = tk.Menu(self.root,tearoff=0)
        
        file_menu = tk.Menu(self.menu_bar,tearoff=0)
        file_menu.add_command(label="打开",command=self.open_file)
        file_menu.add_command(label="保存",command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出",command=self.exit)
        
        help_menu = tk.Menu(self.menu_bar,tearoff=0)
        help_menu.add_command(label="关于我们",command=self.about_us)
        
        self.menu_bar.add_cascade(label="文件",menu=file_menu)
        self.menu_bar.add_cascade(label="帮助",menu=help_menu)
        
        self.root.config(menu=self.menu_bar)
    
    def open_file(self):
        messagebox.showinfo("提示","打开文件！")
    
    def save_file(self):
        messagebox.showinfo("提示","保存文件！")
    
    def exit(self):
        self.root.destroy()
    def about_us(self):
        messagebox.showinfo("提示","一个演示")
    

root = tk.Tk()
app = App(root)
root.mainloop()