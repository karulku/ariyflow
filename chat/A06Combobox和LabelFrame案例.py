import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.create()
    def create(self):
        
        self.name = tk.StringVar()
        self.age = tk.StringVar()
        
        frame1 = tk.LabelFrame(root,text="用户信息",padx=10,pady=10)
        frame1.pack(padx=20,pady=20,fill="both",expand=True)
        tk.Label(frame1,text="姓名：").grid(row=0,column=0,sticky="w")
        tk.Entry(frame1,textvariable=self.name).grid(row=0,column=1,sticky="w",padx=5,pady=5)
        
        tk.Label(frame1,text="年龄：").grid(row=1,column=0,sticky="w")
        tk.Entry(frame1,textvariable=self.age).grid(row=1,column=1,sticky="w",padx=5,pady=5)
        
        tk.Label(frame1,text="性别:").grid(row=2,column=0,sticky="w")
        self.combo = ttk.Combobox(frame1,values=["男","女"],state="readonly")
        self.combo.grid(row=2,column=1,sticky="w",padx=5,pady=5)
        
        btn = tk.Button(frame1,text="click",command=self.btn_event)
        btn.grid(row=3,column=0,columnspan=2)
    
    def btn_event(self):
        print(self.name.get(),self.age.get(),self.combo.get())

root = tk.Tk()
app = App(root)
root.mainloop()