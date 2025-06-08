import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import time

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.geometry("720x500+400+300")
        self.root.title("学习资源管理器")
        
        self.createMenu() # 创建菜单
        self.createData() # 创建需要的数据
        self.createWidgets() # 创建主窗口组件
    
    def createMenu(self):
        menu_bar = tk.Menu(self.root,tearoff=0)
        
        file_menu = tk.Menu(menu_bar,tearoff=0) # 文件栏
        file_menu.add_command(label="导入csv",command=self.file_menu_importcsv)
        file_menu.add_command(label="导出csv",command=self.file_menu_exportcsv)
        file_menu.add_separator()
        file_menu.add_command(label="清空所有资源",command=self.file_menu_clearAllSource)
        file_menu.add_separator()
        file_menu.add_command(label="退出",command=self.file_menu_exit)
        
        set_menu = tk.Menu(menu_bar,tearoff=0) # 设置栏
        set_menu.add_command(label="偏好设置",command=self.set_menu_settings)
        
        help_menu = tk.Menu(menu_bar,tearoff=0) # 帮助栏
        help_menu.add_command(label="关于我们",command=self.help_menu_about_us)
        
        menu_bar.add_cascade(label="文件",menu=file_menu)
        menu_bar.add_cascade(label="设置",menu=set_menu)
        menu_bar.add_cascade(label="帮助",menu=help_menu)        
        self.root.config(menu=menu_bar)
    
    def createData(self):
        self.MAX_TIME = 120 # 学习的最长时间
        self.MIN_TIME = 10 # 学习的最短时间
        self.DEFAULT_STUDY_TIME = 25
        
        self.is_running = False
        
        self.source_name = tk.StringVar() # 资源名称
        self.type_select = tk.StringVar() # 类别选择
        self.url_input = tk.StringVar() # 输入的url
        self.study_time_select = tk.DoubleVar() # 选择的学习时间
        self.time_label = tk.StringVar() # 展示时间的标签
        
        self.settings_default_study_time = tk.DoubleVar() # 设置中的默认学习时长
        self.settings_theme_select = tk.StringVar() # 设置的界面主题
        
        self.study_time_select.set(self.DEFAULT_STUDY_TIME)
        self.time_label.set(f"{int(self.study_time_select.get())}:00")
        self.settings_default_study_time.set(self.DEFAULT_STUDY_TIME)
        self.settings_theme_select.set("light")

    def createWidgets(self):
        
        weights = [0,1,0]
        for i in range(len(weights)):
            self.root.rowconfigure(i,weight=weights[i])
        self.root.columnconfigure(0,weight=1)
        
        frame1 = ttk.LabelFrame(self.root,text="添加学习资源")
        frame1.grid(row=0,column=0,padx=10,pady=5,sticky="we")
        weights = [0,1,0,0,0]
        for i in range(len(weights)):
            frame1.columnconfigure(i,weight=weights[i])
        
        ttk.Label(frame1,text="资源名称：").grid(row=0,column=0,padx=5,pady=3)
        ttk.Entry(frame1,textvariable=self.source_name).grid(row=0,column=1,sticky="we",padx=5,pady=3)
        
        ttk.Label(frame1,text="类别：").grid(row=0,column=2,padx=5,pady=3)
        ttk.Combobox(frame1,textvariable=self.type_select,values=["文章","视频","电子书","课程","其他"],state="readonly").grid(row=0,column=3,padx=5,pady=3)
        ttk.Label(frame1,text="URL: ").grid(row=1,column=0,padx=5,pady=3)
        ttk.Entry(frame1,textvariable=self.url_input).grid(row=1,column=1,padx=5,pady=3,sticky="we")

        ttk.Button(frame1,text="添加资源",command=self.btn_add_source).grid(row=0,column=4,rowspan=2)
        ttk.Button(frame1,text="清空输入",command=self.btn_clear_input).grid(row=0,column=5,rowspan=2)
        
        frame2 = ttk.LabelFrame(self.root,text="资源列表")
        frame2.grid(row=1,column=0,padx=10,pady=5,sticky="wens")
        
        self.treeview_columns = ["资源名称","类别","链接"]
        self.treeview = ttk.Treeview(frame2,columns=self.treeview_columns,show="headings")
        for i in range(len(self.treeview_columns)):
            self.treeview.heading(i,text=self.treeview_columns[i])
        scroll = ttk.Scrollbar(frame2,command=self.treeview.yview)
        self.treeview.config(yscrollcommand=scroll.set)
        scroll.pack(fill='y',side='right')
        self.treeview.pack(padx=5,pady=3,fill="both",expand=True)
        
        frame3 = ttk.LabelFrame(self.root,text="学习计时器",padding=5)
        frame3.grid(row=2,column=0,padx=10,pady=5,sticky="we")
        
        ttk.Label(frame3,text="学习时长（分钟）：").grid(row=0,column=0,padx=5,pady=3)
        self.scale = ttk.Scale(frame3,variable=self.study_time_select,orient="horizontal",from_=self.MIN_TIME,to=self.MAX_TIME,length=200,command=lambda x=self.study_time_select.get():self.update_time_label(float(x)*60//60*60))
        self.scale.grid(row=0,column=1,padx=5,pady=3)
        ttk.Label(frame3,textvariable=self.time_label,width=6,font=("Arial",18)).grid(row=0,column=2,padx=5,pady=3)
        ttk.Button(frame3,text="开始学习",command=self.btn_start_study).grid(row=0,column=3,padx=10,pady=3)
        ttk.Button(frame3,text="重置计时",command=self.btn_restart_time).grid(row=0,column=4,padx=10,pady=3)
    
    def btn_start_study(self):
        if self.is_running:
            messagebox.showinfo("提示","计时已经开始！")
            return
        select = self.treeview.selection()
        # print(select)
        if not select:
            messagebox.showinfo("提示","请先选中一个资源！")
            return
        if len(select) > 1:
            messagebox.showinfo("提示","请不要选择多个资源！")
            return
        self.is_running = True
        self.scale.config(state="disabled")
        self.start_time = time.time()
        self.end_time = self.start_time + self.study_time_select.get()//1*60
        
        def start_timer():
            if self.is_running:
                self.update_time_label(self.end_time-time.time())
                self.root.after(1000,start_timer)
        
        self.root.after(1000,start_timer)

    
    def btn_restart_time(self):
        if not self.is_running:
            messagebox.showinfo("提示","计时未开始！")
            return
        self.is_running = False
        self.scale.config(state="normal")
        self.update_time_label(self.study_time_select.get()//1*60)
    
    def btn_add_source(self):
        name = self.source_name.get()
        type = self.type_select.get()
        url = self.url_input.get()
        if (not name) or (not type) or (not url):
            messagebox.showinfo("提示","请将信息补充完整！")
            return
        self.treeview.insert("",tk.END,values=[name,type,url])
            
    
    def btn_clear_input(self):
        self.source_name.set("")
        self.type_select.set("")
        self.url_input.set("")
    
    def update_time_label(self, time:float):
        """ 传入的time单位为秒 """
        time = int(round(time,0))
        minute = time//60
        sec = time%60
        self.time_label.set(f"{minute:02d}:{sec:02d}")
    
    def file_menu_importcsv(self):
        choice = False
        if self.treeview.get_children():
            choice = messagebox.askyesno("提示","当前列表包含条目是否清除？")

        file_path = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("csv文件","*.csv")])
        if file_path:
            
            if choice:
                for child in self.treeview.get_children():
                    self.treeview.delete(child)
                    
            with open(file_path,mode="r",encoding="utf-8") as file:
                lines = file.readlines()[1:]
                for line in lines:
                    items = [item.strip() for item in line.split(",")]
                    self.treeview.insert("",tk.END,values=items)
                
                messagebox.showinfo("提示","导入成功！")
    
    def file_menu_exportcsv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("csv文件","*.csv")])
        if file_path:
            with open(file_path,mode="a",encoding="utf-8") as file:
                file.write("资源名称，类别，链接\n")
                children = self.treeview.get_children()
                for child in children:
                    items = self.treeview.item(child)["values"]
                    file.write(','.join(items)+"\n")
                
                messagebox.showinfo("提示","保存成功！")
    
    def file_menu_clearAllSource(self):
        choice = messagebox.askyesno("提示","确定要清空全部信息吗？")
        if choice:
            children = self.treeview.get_children()
            for child in children:
                self.treeview.delete(child)
    
    def file_menu_exit(self):
        self.root.destroy()
    
    def set_menu_settings(self):
        win = tk.Toplevel(self.root)
        win.title("设置")
        win.geometry("300x200+400+300")
        
        ttk.Label(win,text="默认学习时长（分钟）：").pack()
        tk.Scale(win,from_=self.MIN_TIME,to=self.MAX_TIME,variable=self.settings_default_study_time,resolution=1,orient="horizontal",length=160).pack()
        
        tk.Label(win,text="界面主题：").pack()
        combo = ttk.Combobox(win,values=["light","dark"],state="readonly")
        combo.pack(pady=5)
        combo.set(self.settings_theme_select.get())
        
        def quit_settings():
            self.DEFAULT_STUDY_TIME = (self.settings_default_study_time.get())*60//60
            self.update_time_label(self.DEFAULT_STUDY_TIME*60)
            win.destroy()

        ttk.Button(win,text="保存并关闭",command=quit_settings).pack(pady=5)
        
        win.transient(self.root)
        win.grab_set()



        
    def help_menu_about_us(self):
        messagebox.showinfo("关于我们","学习资源管理器1.0\nby AriyFlow")
root = tk.Tk()
app = App(root)
root.mainloop()