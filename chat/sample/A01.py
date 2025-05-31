import tkinter as tk
from tkinter import messagebox
import os

TASKS_FILE = "tasks.txt"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # 输入框
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        # 添加按钮
        self.add_btn = tk.Button(root, text="添加任务", width=15, command=self.add_task)
        self.add_btn.pack()

        # 列表框和滚动条
        frame = tk.Frame(root)
        frame.pack()

        self.scrollbar = tk.Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(frame, width=50, height=10, yscrollcommand=self.scrollbar.set)
        self.listbox.pack()

        self.scrollbar.config(command=self.listbox.yview)

        # 删除按钮
        self.del_btn = tk.Button(root, text="删除选中任务", width=15, command=self.delete_task)
        self.del_btn.pack(pady=5)

        # 关闭窗口前保存
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.load_tasks()

    def add_task(self):
        task = self.entry.get().strip()
        if task:
            self.listbox.insert(tk.END, task)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("提示", "任务不能为空！")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
        except IndexError:
            messagebox.showwarning("提示", "请先选择一个任务！")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    task = line.strip()
                    if task:
                        self.listbox.insert(tk.END, task)

    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            tasks = self.listbox.get(0, tk.END)
            for task in tasks:
                f.write(task + "\n")

    def on_close(self):
        self.save_tasks()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
