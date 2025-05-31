import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox

class App:
    def __init__(self, root):
        
        root.title("简易记事本")
        root.geometry("800x500+400+300")
        
        self.create_data()
        self.create_widgets()
    
    def create_data(self):
        self.file_name = tk.StringVar()
    
    def create_widgets(self):
        frame1 = tk.LabelFrame(root,text="文件操作",padx=10,pady=10,height=40)
        frame1.pack(fill="both",padx=10,pady=5)
        tk.Label(frame1,text="文件名：").grid(row=0,column=0)
        tk.Entry(frame1,textvariable=self.file_name).grid(row=0,column=1,sticky="ew",)
        tk.Button(frame1,text="保存",command=self.save_file,relief="groove",width=6,height=1).grid(row=0,column=2)
        tk.Button(frame1,text="加载",command=self.load_file,relief="groove",width=6,height=1).grid(row=0,column=3)
        tk.Button(frame1,text="清空",command=self.clear_text,relief="groove",width=6,height=1).grid(row=0,column=4)
        
        frame1.columnconfigure(1,weight=1) # 让输入文本框随界面大小扩展
        
        frame2 = tk.Frame(root,padx=10,pady=10)
        frame2.pack(fill="both",expand=True,padx=10,pady=5)
        
        scroll = tk.Scrollbar(frame2)
        scroll.pack(side="right",fill="y")
        self.text = tk.Text(frame2,padx=10,pady=10)
        self.text.pack(fill="both",expand=True,padx=10,pady=10)
        
        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        
    def save_file(self): # 保存文件
        file_name = self.file_name.get()
        if not file_name:
            messagebox.showinfo("提示","请输入文件名！")
            return
        if os.path.exists(file_name):
            choice = messagebox.askyesnocancel("提示",f"文件：\"{file_name}\"已存在，确认要替换文件吗？")
            if not choice:
                return
        with open(file_name,mode="w",encoding="utf-8") as file:
            file.write(self.text.get("1.0",tk.END))
            messagebox.showinfo("提示","保存成功！")
    
    def load_file(self):
        file_name = self.file_name.get()
        if not file_name:
            messagebox.showinfo("提示","请输入文件名！")
            return
        if not os.path.exists(file_name):
            messagebox.showinfo("提示",f"文件\"{file_name}\"不存在！")
            return
        with open(file_name,mode="r",encoding="utf-8") as file:
            if self.text.get("1.0",tk.END) != '\n':
                choice = messagebox.askokcancel("提示","加载文件会清空当前内容，确认执行此操作？")
                if not choice:
                    return
            self.text.delete("1.0","end")
            lines = file.readlines()
            for line in lines:
                self.text.insert(tk.END,line)
    def clear_text(self):
        self.text.delete("1.0",'end')
root = tk.Tk()
app = App(root)
root.mainloop()