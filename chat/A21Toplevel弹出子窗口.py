import tkinter as tk
from tkinter import messagebox,ttk,dialog

"""
tkinter.Toplevel 弹出子窗口
    在主窗口之外再打开一个子窗口，用来显示“关于”对话框，设置界面，详细信息等。
    可以实现模态窗口（弹出后必须先关闭它才能返回主窗口）

win = tk.Toplevel(parent)
    新建一个独立于主窗口的顶级容器Toplevel，默认会以新窗口的形式弹出
    可以在这个子窗口里放置任意控件

函数：
win.transient(root) 让这个子窗口始终位于主窗口前面
win.grab_set() 成为模态窗口，先关闭它才能操作主窗口 # 这两个函数合起来用 #

"""

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.geometry("400x300+400+300")
        self.root.title("Toplevel 示例")

        self.createWidgets()
    
    def create_settings_win(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("设置")
        settings_win.geometry("300x200+300+300")
        
        settings_win.transient(root)
        settings_win.grab_set()
        
        ttk.Label(settings_win,text="用户名：").pack(pady=5)
        user_entry = ttk.Entry(settings_win)
        user_entry.pack(pady=5)
        
        ttk.Label(settings_win,text="主题：").pack(pady=5)
        theme_combo = ttk.Combobox(settings_win,values=["浅色","深色"],state="readonly")
        theme_combo.pack(pady=5)
        theme_combo.current(0)
    
    def createWidgets(self):
        tk.Button(self.root,text="打开设置",command=self.create_settings_win,width=6,height=1,relief="groove").pack()

root = tk.Tk()
app = App(root)
root.mainloop()