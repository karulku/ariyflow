import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("用户任务管理器")
        self.root.geometry("680x500+400+300")
        
        self.createData()
        self.createWidgets()
    
    def createData(self):
        self.name=tk.StringVar() # 姓名
        self.age=tk.StringVar() # 年龄
        self.sex=tk.StringVar() # 性别
        self.taskname=tk.StringVar() # 任务名
        self.priority=tk.StringVar() # 优先级
        self.timeVar = tk.StringVar() # 时间变量
        self.job_min = tk.IntVar()
        self.job_min.set(25)
        self.timeVar.set("25:00")
        
        self.is_running = False
        
    
    def createWidgets(self):
        frame1 = tk.LabelFrame(self.root,text="用户信息",padx=5,pady=3,height=60)
        frame1.pack(fill="both",padx=5,pady=3)
        frame1.columnconfigure(1,weight=1)
        tk.Label(frame1,text="姓名：").grid(row=0,column=0)
        tk.Entry(frame1,textvariable=self.name).grid(row=0,column=1,sticky="we",padx=3,pady=2)
        
        tk.Label(frame1,text="年龄：").grid(row=1,column=0)
        tk.Entry(frame1,textvariable=self.age).grid(row=1,column=1,sticky="we",padx=3,pady=2)
        
        tk.Label(frame1,text="性别：").grid(row=2,column=0)
        ttk.Combobox(frame1,values=["男","女"],state="readonly",textvariable=self.sex).grid(row=2,column=1,sticky="we",padx=3,pady=2)
        
        frame2 = tk.LabelFrame(self.root,text="添加任务",padx=5,pady=5,height=60)
        frame2.pack(fill='both',padx=5,pady=3)
        weights = [0,1,0,0,0,0]
        for i in range(len(weights)):
            frame2.columnconfigure(i,weight=weights[i])
        tk.Label(frame2,text="任务名：").grid(row=0,column=0)
        tk.Entry(frame2,textvariable=self.taskname).grid(row=0,column=1,sticky="we")
        tk.Label(frame2,text="优先级：").grid(row=0,column=2)
        combo = ttk.Combobox(frame2,values=["高","中","低"],textvariable=self.priority,state="readonly",width=10)
        combo.grid(row=0,column=3)
        combo.current(0)
        
        tk.Button(frame2,text="添加任务",command=self.add_task,relief="groove",width=6,height=1).grid(row=0,column=4,padx=8,pady=3)
        tk.Button(frame2,text="删除任务",command=self.delete_task,relief="groove",width=6,height=1).grid(row=0,column=5,pady=3)
        
        frame3 = tk.LabelFrame(self.root,text="任务列表",height=10)
        frame3.pack(fill='both',expand=True,padx=5,pady=3)
        
        scroll_bar = tk.Scrollbar(frame3)
        scroll_bar.pack(side='right',fill='y')
        self.listbox = tk.Listbox(frame3)
        self.listbox.pack(fill='both',expand=True)
        
        self.listbox.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=self.listbox.yview)
        
        frame4 = tk.LabelFrame(self.root,text="任务计时器")
        frame4.pack(fill="both",padx=5,pady=3)
        
        self.timeLabel = tk.Label(frame4,textvariable=self.timeVar,font=("Arial",24))
        self.timeLabel.grid(row=0,column=0,columnspan=2,padx=40,sticky="w")

        tk.Button(frame4,text="开始",command=self.start,relief="groove",width=6,height=1).grid(row=0,column=2,padx=10,pady=5)
        tk.Button(frame4,text="重置",command=self.reset,relief="groove",width=6,height=1).grid(row=0,column=3,padx=10,pady=5)
    def add_task(self):
        task_name = self.taskname.get().strip()
        if not task_name:
            messagebox.showinfo("提示","请输入任务名！")
            return
        self.listbox.insert(tk.END,task_name+f" [{self.priority.get()}]")
        
    
    def delete_task(self):
        cur = self.listbox.curselection()
        if not cur:
            messagebox.showinfo("提示","未选中任何内容！")
            return
        self.listbox.delete(cur)
    
    def start(self):
        if self.is_running:
            messagebox.showinfo("提示","程序已经开始！")
            return
        if not self.listbox.curselection():
            messagebox.showinfo("提示","请先选择一个任务！")
            return
        
        self.is_running = True            
        sec = self.job_min.get()*60
        self.start_time = time.time()
        self.end_time = self.start_time+sec
        self.time_start(int(sec))
    
    def time_start(self, t:int):
        if t<=0:
            self.timeVar.set(f"{self.job_min.get()}:00")
            self.is_running = False
            messagebox.showinfo("提示","计时结束！")
            return
        self.timeVar.set(f"{t//60:02d}:{t%60:02d}")
        self.time_after = self.root.after(1000,lambda t=self.end_time-time.time():self.time_start(int(t)))
    
    def reset(self):
        try:
            self.root.after_cancel(self.time_after)
            self.timeVar.set(f"{str(self.job_min.get())}:00")
            self.is_running = False
        except:
            messagebox.showinfo("提示","计时未开始！")
            
    


root = tk.Tk()
app = App(root)
root.mainloop()