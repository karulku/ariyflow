import tkinter as tk
from tkinter import messagebox

class ColorMixer:
    def __init__(self, root):
        self.root = root
        self.root.title("灯光调节面板")
        self.root.geometry("400x300")
        
        self.r = tk.IntVar(value=255)
        self.g = tk.IntVar(value=255)
        self.b = tk.IntVar(value=255)
        
        self.create_widgets()
        self.update_color()
    
    def create_widgets(self):
        # 红色滑动条
        tk.Label(self.root, text="红色").pack()
        tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL,
                 variable=self.r, command=lambda x: self.update_color()).pack(fill="x")
        
        # 绿色滑动条
        tk.Label(self.root, text="绿色").pack()
        tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL,
                 variable=self.g, command=lambda x: self.update_color()).pack(fill="x")
        
        # 蓝色滑动条
        tk.Label(self.root, text="蓝色").pack()
        tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL,
                 variable=self.b, command=lambda x: self.update_color()).pack(fill="x")
        
        # 颜色预览区
        self.color_preview = tk.Label(self.root, text="颜色预览", bg="#FFFFFF", height=5)
        self.color_preview.pack(fill="x", pady=10)
        
        # 按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="重置", command=self.reset_color, width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="保存", command=self.save_color, width=10).pack(side="left", padx=10)
    
    def update_color(self):
        r = self.r.get()
        g = self.g.get()
        b = self.b.get()
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview.config(bg=color_hex)
    
    def reset_color(self):
        self.r.set(255)
        self.g.set(255)
        self.b.set(255)
        self.update_color()
    
    def save_color(self):
        r = self.r.get()
        g = self.g.get()
        b = self.b.get()
        messagebox.showinfo("保存颜色", f"当前颜色 RGB 值：({r}, {g}, {b})")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorMixer(root)
    root.mainloop()