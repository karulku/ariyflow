import tkinter as tk
from tkinter import messagebox,ttk,filedialog
from datetime import datetime

""" 没有任何功能，就是一个界面，后边做tkinter我基本不准备实现了，这玩意调试起来太累了，而且没什么实际作用 """

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.geometry("960x540+400+300")
        self.root.title("🗿 日程仪表盘")
        self.createData()
        self.createWidgets()
    def createData(self):
        
        self.cin01 = tk.StringVar()
        self.time_label = tk.StringVar()
        self.task_title = tk.StringVar()
        self.priority = tk.StringVar()
        self.state_label = tk.StringVar()
        
        self.timeset()
        self.state_label.set("就绪")
    def createWidgets(self):
        frame1 = ttk.LabelFrame(self.root,text="信息")
        frame1.pack(fill="x",padx=10,pady=5)
        weights = [0,1,0]
        for i in range(len(weights)):
            frame1.columnconfigure(i,weight=weights[i])
        self._time_label = ttk.Label(frame1,text="🎣我的日程").grid(row=0,column=0,padx=5,pady=5)
        ttk.Entry(frame1,textvariable=self.cin01).grid(row=0,column=1,padx=5,pady=5,sticky="we")
        ttk.Label(frame1,textvariable=self.time_label).grid(row=0,column=2,padx=5,pady=5)
        
        frame2 = ttk.LabelFrame(self.root,text="工作栏")
        frame2.pack(fill="both",expand=True,padx=10,pady=5)
        
        frame2_1 = ttk.LabelFrame(frame2,text="视图选择",padding=5)
        frame2_1.pack(fill='y',side="left",padx=5,pady=5)
        btn_list = (
            ("今天",self.btn01),
            ("本周",self.btn02),
            ("本月",self.btn03),
            ("已完成",self.btn04)
        )
        for btn in btn_list:
            ttk.Button(frame2_1,text=btn[0],command=btn[1]).pack(pady=5)
        
        frame2_2 = ttk.LabelFrame(frame2,text="当前任务",padding=5)
        frame2_2.pack(fill='both',side='left',padx=5,pady=5,expand=True)
        self.text_scroll = ttk.Scrollbar(frame2_2)
        self.text_scroll.pack(fill="y",side="right")
        
        self.text_area = tk.Text(frame2_2,padx=5,pady=5)
        self.text_area.pack(expand=True,padx=5,pady=5,fill="both")
        
        self.text_area.bind("<Key>",lambda e:"break") # 给键盘数额u绑定break，禁用用户输入

        self.text_area.config(yscrollcommand=self.text_scroll.set)
        self.text_scroll.config(command = self.text_area.yview)
        
        frame2_3 = ttk.LabelFrame(frame2,text="🎞️ 添加新任务",padding=5)
        frame2_3.pack(fill="y",side="left",padx=5,pady=5)
        ttk.Label(frame2_3,text="任务标题：").pack(padx=10,pady=5)
        ttk.Entry(frame2_3,textvariable=self.task_title).pack(padx=10,pady=5)
        ttk.Label(frame2_3,text="概述：").pack(padx=10,pady=5)
        self.task_discription = tk.Text(frame2_3,width=2,height=1)
        self.task_discription.pack(padx=10,pady=5,fill="both",expand=True)
        ttk.Label(frame2_3,text="优先级：").pack(padx=10,pady=5)
        ttk.Combobox(frame2_3,textvariable=self.priority,values=["高","中","低"],state="readonly").pack(padx=10,pady=5)
        ttk.Button(frame2_3,text="添加任务",command=self.addTask).pack(padx=10,pady=5)
        
        frame3 = ttk.LabelFrame(self.root,text="状态栏")
        frame3.pack(fill='x',padx=10,pady=5)
        ttk.Label(frame3,textvariable=self.state_label).pack(side="left",padx=5,pady=5)
    
    def timeset(self):
        t = datetime.now()
        s = t.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.set(s)
        self.root.after(1000,self.timeset)
        self.root.update()
    
    def btn01(self):
        pass
    def btn02(self):
        pass
    def btn03(self):
        pass
    def btn04(self):
        pass
    def addTask(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()