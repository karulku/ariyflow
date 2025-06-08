import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import webbrowser

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.geometry("1080x640+300+200")
        self.root.title("今日热榜")
        self.createStyle()
        self.defConst()
        self.createData()
        self.createWidgets()
    
    def createStyle(self):
        style = ttk.Style()
        style.configure("A.TLabelframe",background="lightgreen")
        style.configure("B.TLabelframe",background="lightblue")
    
    def defConst(self):
        self.where_list = ["全部"]
        self.pageNumSelect = ["1","2","3","4","5","6","7","8","9","10"]
        self.STATE_LIST = ("就绪","获取信息中")
    
    def createData(self):
        self.whereComboText = tk.StringVar() # 选择爬取的网站
        self.pageNum = tk.StringVar() # 要爬取的页数
        self.state = tk.StringVar() # 当前程序的状态
        self.href_message = [] # 保存信息
        self.queue = [] # 序号队列
        self.queueSelect = tk.StringVar()
        
        self.state.set(self.STATE_LIST[0])
    
    def createWidgets(self):
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        
        # 设置栏
        settings_frame = ttk.LabelFrame(self.root,text="设置栏",padding=5)
        settings_frame.grid(row=0,column=0,sticky="we",padx=10,pady=4)
        
        ttk.Label(settings_frame,text="信息来源：",padding=5).grid(row=0,column=0,sticky="e")
        self.where_Combo = ttk.Combobox(settings_frame,values=self.where_list,state="readonly",textvariable=self.whereComboText)
        self.where_Combo.grid(row=0,column=1,padx=10,pady=5,sticky="we")
        self.where_Combo.current(0)
        
        ttk.Label(settings_frame,text="获取页数：").grid(row=0,column=2,padx=5,pady=5)
        self.pageNumCombo = ttk.Combobox(settings_frame,values=self.pageNumSelect,state="readonly",textvariable=self.pageNum)
        self.pageNumCombo.grid(row=0,column=3,padx=10,pady=5)
        self.pageNumCombo.current(0)
        
        ttk.Button(settings_frame,text="获取",command=self.getMessage).grid(row=1,column=0,padx=5,pady=3)
        tk.Label(settings_frame,text="当前状态：").grid(row=1,column=1,sticky="w",padx=10)
        self.stateLabel =  ttk.Label(settings_frame,textvariable=self.state)
        self.stateLabel.grid(row=1,column=1,sticky="e",padx=30)
        
        ttk.Label(settings_frame,text="选择序号：").grid(row=1,column=2)
        self.queueCombo = ttk.Combobox(settings_frame,values=self.queue,state="readonly",textvariable=self.queueSelect)
        self.queueCombo.grid(row=1,column=3)
        ttk.Button(settings_frame,text="进入",command=self.enter_href).grid(row=1,column=4)
        
        # 信息展示框的frame
        self.msg_frame = ttk.LabelFrame(self.root,text="信息栏",padding=5)
        self.msg_frame.grid(row=1,column=0,sticky="wens",padx=10,pady=4)
        
        self.scroll = ttk.Scrollbar(self.msg_frame)
        self.scroll.pack(fill='y',side="right")
        
        view_list = ["序号","信息源","标题","网址"]
        self.treeview = ttk.Treeview(self.msg_frame,columns=view_list,show="headings")
        self.treeview.pack(fill="both",side="left",expand=True,padx=5,pady=5)
        for view in view_list:
            self.treeview.heading(view,text=view)
        self.treeview.column(0,width=10)
        self.treeview.column(1,width=20)
        self.treeview.column(2,width=600,minwidth=400)
        self.treeview.column(3,width=200)
        
        self.scroll.config(command=self.treeview.yview)
        self.treeview.config(yscrollcommand=self.scroll.set)
        

    
    def getMessage(self):
        if self.whereComboText.get() == "全部":
            # messagebox.showinfo("提示","获取全部信息功能开发中...")
            
            # 初始化状态
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            self.queue = []
            
            # 更新状态，进入子程序获取信息
            self.state.set(self.STATE_LIST[1])
            self.root.update()
            proc = subprocess.run(["python","./seleniumGetAll.py",self.pageNum.get()],stdout=subprocess.PIPE,text=True)
            # print("子进程输出内容：\n",proc.stdout)
            lines = proc.stdout.split("\n")
            lines = [line.strip() for line in lines]
            cnt = 1
            for line in lines:
                if line:
                    line = [str(cnt)]+[item.strip() for item in line.split("##--##")]
                    self.href_message.append(line[3])
                    self.treeview.insert("","end",values=line)
                    cnt += 1
            
            # 更新序号队列
            for i in range(1,cnt):
                self.queue.append(i)
            self.queueCombo.config(values=self.queue)
            self.queueSelect.set("")
                
            self.state.set(self.STATE_LIST[0])
            # self.update_msg_frame()
    
    def update_msg_frame(self):
        pass
    
    def enter_href(self):
        idx = int(self.queueSelect.get())
        webbrowser.open(self.href_message[idx-1])
        print(len(self.href_message))
        
        

root = tk.Tk()
app = App(root)
root.mainloop()