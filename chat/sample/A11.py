import tkinter as tk
from tkinter import ttk, messagebox

class FormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("用户信息表单")
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        
        self.create_widgets()
        self.set_form_state("disabled")  # 初始禁用表单

    def create_widgets(self):
        frame = tk.LabelFrame(self.root, text="基本信息", padx=10, pady=10)
        frame.pack(padx=20, pady=20, fill="x")

        tk.Label(frame, text="姓名：").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="年龄：").grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(frame, textvariable=self.age_var)
        self.age_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="性别：").grid(row=2, column=0, sticky="w")
        self.gender_combo = ttk.Combobox(frame, textvariable=self.gender_var, values=["男", "女"], state="readonly")
        self.gender_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        frame.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.edit_btn = tk.Button(btn_frame, text="编辑", command=self.enable_form)
        self.edit_btn.grid(row=0, column=0, padx=10)

        self.submit_btn = tk.Button(btn_frame, text="提交", command=self.submit_form)
        self.submit_btn.grid(row=0, column=1, padx=10)

    def set_form_state(self, state):
        """ 设置控件状态 """
        self.name_entry.config(state=state)
        self.age_entry.config(state=state)
        self.gender_combo.config(state="readonly" if state == "normal" else "disabled")
        self.submit_btn.config(state=state)

    def enable_form(self):
        self.set_form_state("normal")

    def submit_form(self):
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        info = f"姓名：{name}\n年龄：{age}\n性别：{gender}"
        messagebox.showinfo("提交信息", info)
        self.set_form_state("disabled")

# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x250")
    app = FormApp(root)
    root.mainloop()
