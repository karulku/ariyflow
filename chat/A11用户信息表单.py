import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class App:
    def __init__(self, root):
        
        root.geometry("400x240+400+300")
        root.title("用户信息表单")
        self.createData()
        self.createWidgets()
        
    def createData(self):
        self.name = tk.StringVar()
        self.age = tk.StringVar()
        self.sex = tk.StringVar()

    def createWidgets(self):
        frame1 = tk.LabelFrame(root,text="基本信息",padx=10,pady=10)
        frame1.pack(fill='both',expand=True,padx=10,pady=5)
        
        tk.Label(frame1,text="姓名：").grid(row=0,column=0)
        self.name_entry = tk.Entry(frame1,textvariable=self.name,state="disabled")
        self.name_entry.grid(row=0,column=1,sticky="we")
        
        tk.Label(frame1,text="年龄：").grid(row=1,column=0)
        self.age_entry = tk.Entry(frame1,textvariable=self.age,state="disabled")
        self.age_entry.grid(row=1,column=1,sticky="we")
        
        
        tk.Label(frame1,text="性别：").grid(row=2,column=0)
        self.combo = ttk.Combobox(frame1,textvariable=self.sex,values=["男","女"],state="disabled")
        self.combo.grid(row=2,column=1,sticky="we")
        
        frame1.columnconfigure(1,weight=1)
        
        frame2 = tk.Frame(root,padx=10,pady=5)
        frame2.pack(fill="both",expand=True,padx=10,pady=10)
        
        frame2.columnconfigure(0,weight=1)
        frame2.columnconfigure(1,weight=0)
        frame2.columnconfigure(2,weight=0)
        frame2.columnconfigure(3,weight=1)
        tk.Button(frame2,text="编辑",command=self.edit_msg,width=6,height=1,relief="groove").grid(row=0,column=1,padx=5)
        tk.Button(frame2,text="提交",command=self.submit_msg,width=6,height=1,relief="groove").grid(row=0,column=2,padx=5)
    
    def edit_msg(self):
        self.name_entry.config(state="normal")
        self.age_entry.config(state="normal")
        self.combo.config(state="readonly")
    
    def submit_msg(self):
        if self.check_msg_full():
            self.name_entry.config(state="disabled")
            self.age_entry.config(state="disabled")
            self.combo.config(state="disabled")
            messagebox.showinfo("提示",f"提交成功！\n姓名：{self.name_entry.get()}\n年龄：{self.age_entry.get()}\n性别：{self.combo.get()}")
        else:
            messagebox.showinfo("提示","请将信息填写完整！")
    
    def check_msg_full(self):
        if not self.name.get():
            return False
        if not self.age.get():
            return False
        if not self.combo.get():
            return False
        return True

root = tk.Tk()
app = App(root)
root.mainloop()