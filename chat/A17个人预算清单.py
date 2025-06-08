import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        
        self.root.title("个人购物清单+预算管理器")
        self.root.geometry("700x600+400+240")
        
        self.defineConst()
        self.createData()
        self.createWidgets()
    
    def defineConst(self):
        self.BUDGET_BLOOD = 0
        self.BUDGET_CEIL = 10000
    
    def createData(self):
        self.budget = tk.DoubleVar() # 预算
        self.used_money = tk.DoubleVar() # 已使用的钱
        self.used_money_label = tk.StringVar() # 使用金额标签
        self.rest_money_label = tk.StringVar() # 剩余金额标签
        self.product_name = tk.StringVar() # 商品名称
        self.Combo_select = tk.StringVar() # 类型选择
        self.single_price = tk.DoubleVar() # 商品单价
        self.product_num = tk.IntVar() # 商品数量
        
        self.used_money.set(0)
        self.used_money_label.set(f"已用：{round(self.used_money.get(),2)}元")
        self.rest_money_label.set(f"剩余：{round(self.budget.get()-self.used_money.get(),2)}元")
    
    def createWidgets(self):
        frame1 = tk.LabelFrame(self.root,text="设置总预算",padx=5,pady=5,bg="lightgreen")
        frame1.pack(fill='x',padx=5,pady=3)
        
        weights = [0,0,1,1]
        for i in range(len(weights)):
            frame1.columnconfigure(i,weight=weights[i])
        
        tk.Label(frame1,text="总预算（元）：",width=20).grid(row=0,column=0,columnspan=2)
        ttk.Scale(frame1,from_=self.BUDGET_BLOOD,to=self.BUDGET_CEIL,orient="horizontal",variable=self.budget,command=lambda x:self.ScaleUpdate(x)).grid(row=0,column=2,columnspan=2,sticky="we")
        ttk.Label(frame1,textvariable=self.used_money_label,foreground="red").grid(row=1,column=2)
        ttk.Label(frame1,textvariable=self.rest_money_label,foreground="green").grid(row=1,column=3)

        ttk.Entry(frame1,textvariable=self.budget,width=8).grid(row=1,column=0,padx=10,pady=2)
        ttk.Button(frame1,text="设置",command=lambda x=self.budget.get():self.ScaleUpdate(x)).grid(row=1,column=1)
        
        frame2 = tk.LabelFrame(self.root,text="添加购物项",padx=5,pady=5,bg="lightblue")
        frame2.pack(fill='both',padx=5,pady=3)
        
        weights = [0,1,0,1,0,0]
        for i in range(len(weights)):
            frame2.columnconfigure(i,weight=weights[i])
        
        ttk.Label(frame2,text="商品名称：").grid(row=0,column=0,padx=2)
        ttk.Entry(frame2,textvariable=self.product_name).grid(row=0,column=1,padx=20,sticky="we")
        ttk.Label(frame2,text="分类：").grid(row=0,column=2,padx=2)
        ttk.Combobox(frame2,values=["日常用品","食品饮料","服装鞋帽","电子产品","其他"],state="readonly",textvariable=self.Combo_select).grid(row=0,column=3,padx=20,sticky="we")
        ttk.Label(frame2,text="单价（元）：").grid(row=1,column=0)
        ttk.Entry(frame2,textvariable=self.single_price).grid(row=1,column=1,sticky="we",padx=20)
        
        ttk.Label(frame2,text="数量：").grid(row=1,column=2)
        ttk.Entry(frame2,textvariable=self.product_num).grid(row=1,column=3,sticky="we",padx=20)
        
        ttk.Button(frame2,text="添加",command=self.add_item).grid(row=0,column=4,rowspan=2,padx=5)
        ttk.Button(frame2,text="清空输入",command=self.clear_input).grid(row=0,column=5,rowspan=2,padx=5)
        
        frame3 = tk.LabelFrame(self.root,text="购物清单",bg="pink")
        frame3.pack(fill="both",expand=True,padx=5,pady=3)
        self.scroll = ttk.Scrollbar(frame3)
        self.scroll.pack(fill='y',side="right")
        # self.listbox = tk.Listbox(frame3)
        # self.listbox.pack(fill="both",expand=True)
        show_list = ["商品","分类","单价（元）","数量","小计（元）"]
        self.treeview = ttk.Treeview(frame3,columns=show_list,show="headings")
        self.treeview.pack(fill="both",expand=True)
        for i in range(len(show_list)):
            self.treeview.heading(show_list[i],text=show_list[i])
            self.treeview.column(show_list[i],width=10)
        
        self.treeview.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.treeview.yview)
        
        frame4 = tk.Frame(self.root,padx=5,pady=5,bg="lightgray")
        frame4.pack(fill="x",side="bottom")
        ttk.Button(frame4,text="删除选中项",command=self.delete_select_item).grid(row=0,column=0,padx=10,pady=5)
        ttk.Button(frame4,text="清空所有项",command=self.clear_all_item).grid(row=0,column=1,padx=10,pady=5)
    
    def ScaleUpdate(self,x):
        self.used_money_label.set(f"已用：{round(self.used_money.get(),2)}元")
        self.rest_money_label.set(f"剩余：{round(self.budget.get()-self.used_money.get(),2)}元")
    
    def add_item(self):
        try:
            name = self.product_name.get()
            select = self.Combo_select.get()
            single = self.single_price.get()
            num = self.product_num.get()
            sum_money = round(single*num,2)
            if not all([name,select,single,num]):
                messagebox.showinfo("提示","请将信息输入完整！")
                return
        except:
            messagebox.showinfo("提示","请检查输入信息是否正确！")
            return
        self.treeview.insert("","end",values=(name,select,single,num,sum_money))
        self.used_money.set(self.used_money.get()+sum_money)
        self.ScaleUpdate(self.budget.get())
        if self.used_money.get() > self.budget.get():
            messagebox.showinfo("提示","当前金额已超过预算！")
    
    def clear_input(self):
        self.product_name.set("")
        self.Combo_select.set("")
        self.single_price.set(0)
        self.product_num.set(0)
    
    def delete_select_item(self):
        selects = self.treeview.selection()
        if not selects:
            messagebox.showinfo("提示","请先选中要删除的条目！")
            return
        for select in selects:
            sum_money = float(self.treeview.item(select)["values"][4])
            self.used_money.set(self.used_money.get() - sum_money)
            self.treeview.delete(select)
        self.ScaleUpdate(self.budget.get())
            
            
    
    def clear_all_item(self):
        choice = messagebox.askyesno("提示","确认要清空所有项吗？")
        if choice:
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            self.used_money.set(0)


root = tk.Tk()
app = App(root)
root.mainloop()