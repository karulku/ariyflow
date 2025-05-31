import tkinter as tk
from tkinter import ttk
import os

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("简易记事本")
        self.filename = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # 顶部输入区
        input_frame = tk.LabelFrame(self.root, text="文件操作", padx=10, pady=5)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="文件名：").grid(row=0, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.filename).grid(row=0, column=1, sticky="we", padx=5)
        input_frame.columnconfigure(1, weight=1)

        tk.Button(input_frame, text="保存", command=self.save_file).grid(row=0, column=2, padx=5)
        tk.Button(input_frame, text="加载", command=self.load_file).grid(row=0, column=3, padx=5)
        tk.Button(input_frame, text="清空", command=self.clear_text).grid(row=0, column=4, padx=5)

        # 文本编辑区
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text = tk.Text(text_frame, wrap="word")
        self.text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

    def save_file(self):
        filename = self.filename.get().strip()
        if filename:
            content = self.text.get("1.0", tk.END)
            with open(f"{filename}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"保存为 {filename}.txt")
        else:
            print("请输入文件名")

    def load_file(self):
        filename = self.filename.get().strip()
        if filename and os.path.exists(f"{filename}.txt"):
            with open(f"{filename}.txt", "r", encoding="utf-8") as f:
                content = f.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            print(f"加载了 {filename}.txt")
        else:
            print("文件不存在")

    def clear_text(self):
        self.text.delete("1.0", tk.END)

# 运行
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = NotepadApp(root)
    root.mainloop()