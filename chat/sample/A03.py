import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("简易记事本")
        self.root.geometry("600x400")

        self.text_area = tk.Text(root, undo=True, font=("Arial", 12))
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        self.file_path = None

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="打开", command=self.open_file)
        file_menu.add_command(label="保存", command=self.save_file)
        file_menu.add_command(label="另存为", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menu_bar.add_cascade(label="文件", menu=file_menu)

        # 编辑菜单
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="撤销", command=self.text_area.edit_undo)
        edit_menu.add_command(label="重做", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="剪切", command=lambda: self.root.focus_get().event_generate('<<Cut>>'))
        edit_menu.add_command(label="复制", command=lambda: self.root.focus_get().event_generate('<<Copy>>'))
        edit_menu.add_command(label="粘贴", command=lambda: self.root.focus_get().event_generate('<<Paste>>'))
        menu_bar.add_cascade(label="编辑", menu=edit_menu)

        self.root.config(menu=menu_bar)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.file_path = path
                self.root.title(f"简易记事本 - {path}")
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件：{e}")

    def save_file(self):
        if self.file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo("保存成功", "文件已保存。")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.file_path = path
                self.root.title(f"简易记事本 - {path}")
                messagebox.showinfo("保存成功", "文件已另存为。")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNotepad(root)
    root.mainloop()
