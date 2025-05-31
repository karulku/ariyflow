import tkinter as tk
from tkinter import ttk, messagebox
import time

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("用户任务管理器")
        self.root.geometry("600x500")
        
        self.create_vars()
        self.create_widgets()
        self.timer_id = None
        self.is_timer_running = False
        self.end_time = 0
        
    def create_vars(self):
        # 用户信息变量
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.sex_var = tk.StringVar()
        
        # 任务输入变量
        self.task_name_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="中")
        
        # 计时变量
        self.time_var = tk.StringVar(value="00:00")
        
        # 任务存储：list of dict {name, priority}
        self.tasks = []
        
    def create_widgets(self):
        # 用户信息区
        user_frame = tk.LabelFrame(self.root, text="用户信息", padx=10, pady=10)
        user_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        tk.Label(user_frame, text="姓名:").grid(row=0, column=0, sticky="w")
        tk.Entry(user_frame, textvariable=self.name_var).grid(row=0, column=1, sticky="ew", padx=5)
        
        tk.Label(user_frame, text="年龄:").grid(row=1, column=0, sticky="w")
        tk.Entry(user_frame, textvariable=self.age_var).grid(row=1, column=1, sticky="ew", padx=5)
        
        tk.Label(user_frame, text="性别:").grid(row=2, column=0, sticky="w")
        self.sex_combo = ttk.Combobox(user_frame, textvariable=self.sex_var, values=["男", "女", "其他"], state="readonly")
        self.sex_combo.grid(row=2, column=1, sticky="ew", padx=5)
        
        user_frame.columnconfigure(1, weight=1)
        
        # 任务输入区
        task_frame = tk.LabelFrame(self.root, text="添加任务", padx=10, pady=10)
        task_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        tk.Label(task_frame, text="任务名:").grid(row=0, column=0, sticky="w")
        tk.Entry(task_frame, textvariable=self.task_name_var).grid(row=0, column=1, sticky="ew", padx=5)
        
        tk.Label(task_frame, text="优先级:").grid(row=0, column=2, sticky="w", padx=(20,0))
        priority_combo = ttk.Combobox(task_frame, textvariable=self.priority_var, values=["高", "中", "低"], state="readonly", width=6)
        priority_combo.grid(row=0, column=3, sticky="w", padx=5)
        
        add_btn = tk.Button(task_frame, text="添加任务", command=self.add_task)
        add_btn.grid(row=0, column=4, sticky="w", padx=10)
        
        task_frame.columnconfigure(1, weight=1)
        
        # 任务列表区
        list_frame = tk.LabelFrame(self.root, text="任务列表", padx=10, pady=10)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        self.task_listbox = tk.Listbox(list_frame, height=10)
        self.task_listbox.grid(row=0, column=0, sticky="nsew")
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 计时器区
        timer_frame = tk.LabelFrame(self.root, text="任务计时器", padx=10, pady=10)
        timer_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        self.timer_label = tk.Label(timer_frame, textvariable=self.time_var, font=("Arial", 28))
        self.timer_label.grid(row=0, column=0, columnspan=3)
        
        self.start_btn = tk.Button(timer_frame, text="开始", command=self.start_timer, width=10)
        self.start_btn.grid(row=1, column=0, pady=10)
        
        self.reset_btn = tk.Button(timer_frame, text="重置", command=self.reset_timer, width=10)
        self.reset_btn.grid(row=1, column=1, pady=10)
        
        timer_frame.columnconfigure(0, weight=1)
        timer_frame.columnconfigure(1, weight=1)
        
        # 根窗口布局配置，让任务列表区可扩展
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
    
    def add_task(self):
        name = self.task_name_var.get().strip()
        priority = self.priority_var.get()
        if not name:
            messagebox.showwarning("错误", "任务名称不能为空！")
            return
        self.tasks.append({"name": name, "priority": priority})
        self.task_listbox.insert(tk.END, f"{name} [{priority}]")
        self.task_name_var.set("")
        messagebox.showinfo("成功", f"任务“{name}”添加成功！")
    
    def on_task_select(self, event):
        # 选中任务后自动重置计时器显示为默认专注时间25:00
        self.reset_timer()
    
    def start_timer(self):
        if self.is_timer_running:
            messagebox.showinfo("提示", "计时器已运行")
            return
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一个任务！")
            return
        
        # 计时25分钟（1500秒）
        self.countdown(1500)
    
    def countdown(self, remaining_seconds):
        if remaining_seconds < 0:
            messagebox.showinfo("完成", "专注时间结束！")
            self.is_timer_running = False
            self.time_var.set("00:00")
            return
        self.is_timer_running = True
        mins, secs = divmod(remaining_seconds, 60)
        self.time_var.set(f"{mins:02d}:{secs:02d}")
        self.timer_id = self.root.after(1000, self.countdown, remaining_seconds - 1)
    
    def reset_timer(self):
        if self.is_timer_running:
            self.root.after_cancel(self.timer_id)
            self.is_timer_running = False
        self.time_var.set("25:00")  # 默认25分钟
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
