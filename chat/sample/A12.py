import tkinter as tk
from tkinter import ttk, messagebox

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("番茄钟 Pomodoro Timer")
        self.root.geometry("350x250")

        # 默认时长（分钟）
        self.work_minutes = tk.StringVar(value="25")
        self.break_minutes = tk.StringVar(value="5")

        self.is_running = False
        self.remaining_seconds = 0
        self.timer_id = None

        self.create_widgets()

    def create_widgets(self):
        # ==== 参数设置区 ====
        param_frame = tk.LabelFrame(self.root, text="设置时长 (分钟)", padx=10, pady=10)
        param_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(param_frame, text="专注：").grid(row=0, column=0, sticky="e")
        self.work_entry = tk.Entry(param_frame, width=5, textvariable=self.work_minutes)
        self.work_entry.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(param_frame, text="休息：").grid(row=1, column=0, sticky="e")
        self.break_entry = tk.Entry(param_frame, width=5, textvariable=self.break_minutes)
        self.break_entry.grid(row=1, column=1, sticky="w", padx=5)

        param_frame.columnconfigure(1, weight=1)

        # ==== 倒计时显示区 ====
        self.time_label = tk.Label(self.root, text="00:00", font=("Arial", 40))
        self.time_label.pack(pady=10)

        # ==== 控制按钮区 ====
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.start_btn = tk.Button(btn_frame, text="开始", width=8, command=self.toggle_timer)
        self.start_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(btn_frame, text="重置", width=8, command=self.reset_timer)
        self.reset_btn.pack(side="left", padx=5)

    def toggle_timer(self):
        if not self.is_running:
            # 开始
            try:
                work = int(self.work_minutes.get())
                brk = int(self.break_minutes.get())
            except ValueError:
                messagebox.showwarning("错误", "请输入合法的整数时长")
                return
            # 第一次启动，设为专注时长
            if self.remaining_seconds == 0:
                self.remaining_seconds = work * 60
            self.is_running = True
            self.start_btn.config(text="暂停")
            # 禁用输入
            self.work_entry.config(state="disabled")
            self.break_entry.config(state="disabled")
            self.count_down()
        else:
            # 暂停
            self.is_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.start_btn.config(text="继续")

    def count_down(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.timer_id = self.root.after(1000, self.count_down)
        else:
            # 专注或休息阶段结束
            period = "专注" if self.start_btn.cget("text") in ("暂停",) else "休息"
            messagebox.showinfo("提示", f"{period}时间到！")
            # 切换到下一个阶段
            if period == "专注":
                self.remaining_seconds = int(self.break_minutes.get()) * 60
                self.start_btn.config(text="暂停")
                self.count_down()
            else:
                self.finish_cycle()

    def finish_cycle(self):
        # 完成一个专注+休息周期
        self.is_running = False
        self.start_btn.config(text="开始")
        self.work_entry.config(state="normal")
        self.break_entry.config(state="normal")
        self.remaining_seconds = 0
        self.time_label.config(text="00:00")

    def reset_timer(self):
        # 取消定时器
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.remaining_seconds = 0
        self.time_label.config(text="00:00")
        self.start_btn.config(text="开始")
        self.work_entry.config(state="normal")
        self.break_entry.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
