import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
"""
state用于设置控件的当前状态

normal 默认状态
disabled 禁用，不能点击/编辑
readonly 只对ttk.Combobox有效，用户不能手动输入，只能选择
"""

class App:
    def __init__(self, root):
        self.create()
        self.turn = 0
    def create(self):
        # 禁用entry输入框
        root.geometry("400x200+400+300")
        tk.Entry(root,state="disabled").pack()
        
        # 设置Button失效
        self.btn = tk.Button(root,text="click",state="disabled",relief="groove",width=6,height=1,command=self.btn_event1)
        self.btn.pack()
        self.btn.after(100,self.btn_after1)
        
        # 将Text区域设置为只读
        text = tk.Text(root,width=10,height=10)
        text.insert(tk.END,"只读文本内容")
        text.config(state="disabled")
        text.pack(fill='both',expand=True)
        
        combo = ttk.Combobox(root,values=["A","B","C","D"],state="readonly")
        combo.pack()
    
    def btn_after1(self):
        self.turn = 1-self.turn
        if self.turn:
            self.btn.config(state="normal")
        else:
            self.btn.config(state="disabled")
        self.btn.after(100,self.btn_after1)
    
    def btn_event1(self):
        messagebox.showinfo("提示","你点击到我了！")
        

root = tk.Tk()
app = App(root)
root.mainloop()