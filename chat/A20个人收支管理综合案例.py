import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv

class App:
    def __init__(self,root:tk.Tk):
        self.root = root
        self.createData()
        self.createMenu()
        self.createWidgets()
    
    def createData(self):
        self.treeviewColumn = ["金额","类型","分类"]
        self.typeValues = ["收入","支出"]
        self.classifyValues = ["工资","购物","饮食","交通","娱乐","其他"]
        
        self.set_money = tk.DoubleVar() # 用户设置的金额
        self.type_select = tk.StringVar() # 用户选择的类型
        self.classify_select = tk.StringVar() # 用户选择的分类
        self.rest_money_label = tk.StringVar() # 右下角显示的余额
        self.sum_money = 0.0 # 总钱数
        
        self.rest_money_label.set("余额：0.0元")
    
    def createMenu(self):
        menu_bar = tk.Menu(self.root,tearoff=0)
        
        file_menu = tk.Menu(menu_bar,tearoff=0) # 文件菜单
        file_menu.add_command(label="导出记录",command=self.output_record)
        file_menu.add_command(label="清空记录",command=self.clear_record)
        file_menu.add_separator()
        file_menu.add_command(label="退出",command=self.exit)
        
        help_menu = tk.Menu(menu_bar,tearoff=0) # 帮助菜单
        help_menu.add_command(label="关于我们",command=self.about_us)
        
        menu_bar.add_cascade(label="文件",menu=file_menu)
        menu_bar.add_cascade(label="帮助",menu=help_menu)
        self.root.config(menu=menu_bar)
    
    def createWidgets(self):
        frame1 = tk.LabelFrame(self.root,text="添加条目")
        frame1.pack(fill="x",padx=10,pady=5)
        
        weights = [0,1,0,1,0,1,0]
        for i in range(len(weights)):
            frame1.columnconfigure(i,weight=weights[i])
        
        ttk.Label(frame1,text="金额（元）：").grid(row=0,column=0,padx=2)
        ttk.Entry(frame1,textvariable=self.set_money).grid(row=0,column=1,padx=2,sticky="we")
        ttk.Label(frame1,text="类型：").grid(row=0,column=2,padx=2)
        ttk.Combobox(frame1,values=self.typeValues,state="readonly",textvariable=self.type_select).grid(row=0,column=3,padx=2,sticky="we")
        ttk.Label(frame1,text="分类：").grid(row=0,column=4,padx=2)
        ttk.Combobox(frame1,values=self.classifyValues,textvariable=self.classify_select,state="readonly").grid(row=0,column=5,padx=2,sticky="we")
        ttk.Button(frame1,text="添加",command=self.add_item).grid(row=0,column=6,padx=2)
        
        frame2 = tk.Frame(self.root)
        frame2.pack(fill="both",expand=True,padx=10,pady=5)
        
        
        self.treeview = ttk.Treeview(frame2,columns=self.treeviewColumn,show="headings")
        for i in range(len(self.treeviewColumn)):
            self.treeview.heading(i,text=self.treeviewColumn[i])
            
        self.scroll = ttk.Scrollbar(frame2)
        self.scroll.pack(fill="y",side="right")
        self.treeview.pack(fill="both",expand=True)
        
        self.treeview.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.treeview.yview)
        
        ttk.Button(self.root,text="删除选中",command=self.delete_select_item).pack(side="left",padx=10,pady=5)
        ttk.Label(self.root,textvariable=self.rest_money_label).pack(side="right",padx=10,pady=5)
    
    def delete_select_item(self): # 主界面删除选中按钮
        selects = self.treeview.selection()
        if not selects:
            messagebox.showinfo("提示","未选中任何条目！")
            return
        for select in selects:
            item = self.treeview.item(select,"values")
            if item[1] == "收入":
                self.sum_money -= float(item[0])
            else:
                self.sum_money += float(item[0])
            self.treeview.delete(select)
        
        self.rest_money_label.set(f"余额：{round(self.sum_money,2)}元")
    
    def add_item(self): # 主界面添加按钮
        money = self.set_money.get()
        type = self.type_select.get()
        classify = self.classify_select.get()
        if (not type) or (not classify):
            messagebox.showinfo("提示","请将信息补充完整！")
            return
        if money < 0:
            messagebox.showinfo("提示","金额必须为正！")
            return
        self.treeview.insert("",tk.END,values=[money,type,classify])
        if type == "收入":
            self.sum_money += money
        else:
            self.sum_money -=  money
        self.rest_money_label.set(f"余额：{round(self.sum_money,2)}元")

    
    def output_record(self): # 菜单-文件-导出记录
        filepath = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV 文件","*.csv")])
        if not filepath:
            return
        with open(filepath,mode="w",encoding="utf-8",newline="") as file:
            children = self.treeview.get_children()
            writer = csv.writer(file)
            writer.writerow(["金额","类型","分类"])
            for child in children:
                writer.writerow(self.treeview.item(child)["values"])
            messagebox.showinfo("导出成功",f"数据已导出到：\n{filepath}")
    
    def clear_record(self): # 菜单-文件-清空记录
        choice = messagebox.askyesno("提示","确定要清空所有条目吗？")
        if choice:
            items = self.treeview.get_children()
            for item in items:
                self.treeview.delete(item)
            self.sum_money = 0.0
            self.rest_money_label.set(f"余额：0.0元")
    
    def exit(self): # 菜单-文件-退出
        self.root.destroy()
    
    def about_us(self): # 关于我们
        messagebox.showinfo("提示","技术支持：Tkinter")
root = tk.Tk()
app = App(root)
root.mainloop()