import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        
        self.root.title("番茄钟")
        self.root.geometry("360x240+400+300")
        self.createData()
        self.createWidgets()
    
    def createData(self):
        self.job_min = tk.StringVar()
        self.rest_min = tk.StringVar()
        self.timeVar = tk.StringVar()
        self.statusVar = tk.StringVar()
        self.statusVar.set("等待开始...")
        self.timeVar.set("00:00")
        self.job_min.set("1")
        self.rest_min.set("1")
        self.turn = 1
        self.afterID = None
        self.is_start = False
        
    def createWidgets(self):
        frame1 = tk.LabelFrame(self.root,text="设置时长（分钟）",padx=10,pady=10,bg="lightblue")
        frame1.pack(fill='both',expand=True,padx=10,pady=5)
        tk.Label(frame1,text="专注：").grid(row=0,column=0)
        tk.Entry(frame1,textvariable=self.job_min,width=6).grid(row=0,column=1,sticky="w")
        
        tk.Label(frame1,text="休息：").grid(row=1,column=0)
        tk.Entry(frame1,textvariable=self.rest_min,width=6).grid(row=1,column=1,sticky="w")
        
        frame2 = tk.Frame(self.root,padx=10,pady=10,bg="lightgreen")
        frame2.pack(expand=True,padx=10,pady=5,fill="both")
        weights = [1,0,0,1]
        for i in range(len(weights)):
            frame2.columnconfigure(i,weight=weights[i])
        tk.Label(frame2,textvariable=self.timeVar,padx=10,pady=5,font=("Arial",32)).grid(row=0,column=1,columnspan=2)
        tk.Label(frame2,textvariable=self.statusVar,width=12).grid(row=0,column=0,sticky="nw")
        tk.Button(frame2,text="开始",command=self.start,width=6,height=1,relief="groove").grid(row=1,column=1,padx=10,pady=5)
        tk.Button(frame2,text="重置",command=self.reset,width=6,height=1,relief="groove").grid(row=1,column=2,padx=10,pady=5)
    
    def start(self):
        if self.is_start:
            messagebox.showinfo("提示","程序已经开始！")
            return
        self.is_start = True
        job_min = 0
        rest_min = 0
        
        try:
            job_min = int(self.job_min.get())
            rest_min = int(self.rest_min.get())
        except:
            messagebox.showinfo("提示","请输入正确的时间！")
            return
        
        if self.turn:# 专注时间
            self.statusVar.set("当前状态：专注")
            self.start_time = time.time()
            self.end_time = time.time()+(job_min*60)
            self.updateTime(int(self.end_time-self.start_time))
        else: # 休息时间
            self.statusVar.set("当前状态：休息")
            self.start_time = time.time()
            self.end_time = time.time()+(rest_min*60)
            self.updateTime(int(self.end_time-self.start_time))
    
    def updateTime(self,t:int):
        if t<=0:
            if self.turn:
                messagebox.showinfo("提示","专注时间时间结束！")
            else:
                messagebox.showinfo("提示","休息时间结束！")
            self.turn = 1-self.turn
            self.start()
            return
        # print(t)
        self.timeVar.set(f"{t//60:02d}:{t%60:02d}")
        self.afterID = self.root.after(1000,lambda tim=self.end_time-time.time(): self.updateTime(int(tim)))
    
    def reset(self):
        if self.afterID:
            self.root.after_cancel(self.afterID)
            self.afterID = None
            self.statusVar.set("等待开始...")
        try:
            t = int(self.job_min.get())*60
        except:
            t = 0
        self.timeVar.set(f"{t//60:02d}:{t%60:02d}")
        self.is_start = False
        
root = tk.Tk()
app = App(root)
root.mainloop()