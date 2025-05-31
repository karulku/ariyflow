import tkinter as tk
from tkinter import messagebox
import os
import time

TASKS_FILE_PATH = "./msg/task.txt"

class TodoApp:
    def __init__(self,root):
        self.root = root
        
        self.createData()
        self.createWidgets()
    
    def createData(self):
        self.SAVE_INTERVAL = 10
        self.load_last_time = 0
    
    def createWidgets(self):
        self.entry = tk.Entry(self.root,width=40)
        self.entry.pack(pady=10)
        
        self.add_btn = tk.Button(self.root,text="添加任务",command = self.add_task)
        self.add_btn.pack()
        
        frame = tk.Frame(self.root)
        frame.pack()
        
        self.scrollbar = tk.Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.listbox = tk.Listbox(frame,yscrollcommand=self.scrollbar.set)
        self.listbox.pack()
        
        self.scrollbar.config(command=self.listbox.yview)
        
        self.del_btn = tk.Button(root,text="删除选中的任务",command = self.delete_task)
        self.del_btn.pack(pady=5)
        
        root.protocol("WM_CLOSE_WINDOW",self.closeWindow)
        self.load_tasks()
    
    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.save_tasks()
        except:
            messagebox.showerror("提示","请先选择一条信息！")

    def closeWindow(self):
        self.save_tasks()
        root.destroy()
    
    def save_tasks(self):
        self.now_time = time.time()
        print(self.now_time,self.load_last_time)
        if self.now_time - self.load_last_time < self.SAVE_INTERVAL:
            return
        
        with open(TASKS_FILE_PATH,"w",encoding="utf-8") as file:
            tasks = self.listbox.get(0,"end")
            for task in tasks:
                file.write(task.strip()+"\n")
        self.load_last_time = time.time()
    def load_tasks(self):
        with open(TASKS_FILE_PATH,"r",encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                self.listbox.insert("end",line.strip())
    def add_task(self):
        if self.entry.get():
            self.listbox.insert("end",self.entry.get())
            self.save_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.title("Todo-List")
    root.mainloop()