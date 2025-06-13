import tkinter as tk
from tkinter import messagebox,ttk,filedialog

"""
只做了UI，具体功能没有实现
"""

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("英语单词背诵助手")
        self.createData()
        self.createWidgets()
        self.createMenu()

    def createData(self):
        """ 常量部分 """
        self.part = ["名词","动词","形容词","副词","其他"]
        self.treeviewColumn = ["英文","词性","中文"]
        self.stateList = ["未开始测试","测试已开始！"]
        self.winTheme = ["light","dark"]
        
        """ 设置可以修改的部分 """
        self.floor_time = 0
        self.ceil_time = 60
        
        """ 程序运行需要变化的部分 """
        self.wordEntry = tk.StringVar() # 输入的单词
        self.wordTrans = tk.StringVar() # 输入的单词翻译
        self.time_label = tk.StringVar(value="00:00") # 展示的时间标签
        self.state_label = tk.StringVar(value=self.stateList[0]) # 展示的状态标签
        self.setting_testMin = tk.StringVar() # 设置--默认测试时长
        self.setting_winTheme = tk.StringVar() # 设置--界面主题
        
    def createWidgets(self):
        """ 添加新单词的框架 """
        frame1 = ttk.Labelframe(self.root,text="添加新单词")
        frame1.pack(padx=10,pady=5,fill='x')
        ttk.Label(frame1,text="英文：").pack(side="left",padx=5,pady=5)
        ttk.Entry(frame1,textvariable=self.wordEntry).pack(side="left",padx=5,pady=5,fill='x',expand=True)
        ttk.Label(frame1,text="词性").pack(side="left",padx=5,pady=5)
        self.combo = ttk.Combobox(frame1,values=self.part,state="readonly").pack(side="left",padx=5,pady=5,fill='x',expand=True)
        ttk.Label(frame1,text="中文：").pack(side="left",padx=5,pady=5)
        ttk.Entry(frame1,textvariable=self.wordTrans).pack(side="left",fill='x',expand=True,padx=5,pady=5)
        ttk.Button(frame1,text="添加",command=self.btn_add).pack(side="left",padx=5,pady=5)
        ttk.Button(frame1,text="删除选中",command=self.btn_delete).pack(side="left",padx=5,pady=5)

        """ 单词列表的框架 """
        frame2 = ttk.Labelframe(self.root,text="单词列表")
        frame2.pack(fill="both",expand=True,padx=10,pady=5)
        
        scroll = ttk.Scrollbar(frame2)
        self.treeview = ttk.Treeview(frame2,columns=self.treeviewColumn,show="headings")
        scroll.pack(fill="y",side="right")
        self.treeview.pack(padx=5,pady=5,expand=True,fill="both")
        self.treeview.config(yscrollcommand=scroll.set)
        scroll.config(command=self.treeview.yview)
        for i in range(len(self.treeviewColumn)):
            self.treeview.heading(i,text=self.treeviewColumn[i])
        
        """ 背诵测试框架 """
        frame3 = ttk.Labelframe(self.root,text="背诵测试")
        frame3.pack(fill='x',padx=10,pady=5)
        ttk.Label(frame3,text="时长(min)：").pack(side="left",padx=5,pady=5)
        ttk.Scale(frame3,from_=self.floor_time,to=self.ceil_time,length=200).pack(side="left",padx=5,pady=5)
        ttk.Label(frame3,textvariable=self.time_label,font=("Arial",18)).pack(side="left",padx=5,pady=5)
        ttk.Button(frame3,text="开始测试",command=self.btn_StartTest).pack(side="left",padx=5,pady=5)
        ttk.Button(frame3,text="重置",command=self.btn_reset).pack(side="left",padx=5,pady=5)
        
        ttk.Label(self.root,textvariable=self.state_label).pack(side="left",padx=10,pady=5)
    
    def createMenu(self):
        """ 创建菜单 """
        menu = tk.Menu(self.root,tearoff=0)
        
        """ 文件菜单 """
        file_menu = tk.Menu(menu,tearoff=0)
        file_menu.add_command(label="导入csv",command=self.import_csv)
        file_menu.add_command(label="导出csv",command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="退出",command=self.exit_program)
        
        """ 设置菜单 """
        setting_menu = tk.Menu(menu,tearoff=0)
        setting_menu.add_command(label="偏好设置",command=self.setting_topLevel)
        
        """ 帮助菜单 """
        help_menu = tk.Menu(menu,tearoff=0)
        help_menu.add_command(label="关于",command=lambda:messagebox.showinfo("提示","单词背诵助手1.0"))
        
        menu.add_cascade(label="文件",menu=file_menu)
        menu.add_cascade(label="设置",menu=setting_menu)
        menu.add_cascade(label="帮助",menu=help_menu)
        
        self.root.config(menu=menu)
        
    def btn_add(self):
        pass
    def btn_delete(self):
        pass
    def btn_reset(self):
        pass
    def btn_StartTest(self):
        pass
    def import_csv(self):
        pass
    def export_csv(self):
        pass
    def exit_program(self):
        pass
    def setting_save(self):
        pass
    def setting_topLevel(self):
        """ 设置界面 """
        settings_win = tk.Toplevel(self.root)
        settings_win.title("设置")
        settings_win.geometry("+400+300")
        settings_win.transient()
        settings_win.grab_set()
        settings_win.resizable(False,False)
        settings_win.columnconfigure(1,weight=1)
        ttk.Label(settings_win,text="默认测试时长(分钟)：").grid(row=0,column=0,padx=5,pady=5)
        ttk.Entry(settings_win,textvariable=self.setting_testMin).grid(row=0,column=1,padx=5,pady=5,sticky="we")
        ttk.Label(settings_win,text="界面主题：").grid(row=1,column=0,padx=5,pady=5)
        ttk.Combobox(settings_win,values=self.winTheme,state="readonly").grid(row=1,column=1,padx=5,pady=5,sticky="we")
        ttk.Button(settings_win,text="保存",command=self.setting_save).grid(row=2,column=0,columnspan=2,pady=5)
        
root = tk.Tk()
app = App(root)
root.mainloop()