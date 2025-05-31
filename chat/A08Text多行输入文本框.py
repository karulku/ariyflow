import tkinter as tk
from tkinter import messagebox
"""
插入文本 text.insert(index,content)
获取全部内容 text.get("1.0",tk.END)
删除内容 text.delete("1.0",tk.END)
设置只读 text.config(state = "disabled")
重新可编辑 text.config(state = "normal")
插入光标位置 "insert"
行列坐标格式 "行.列" 比如"1.0"表示第一行开头，行从1开始数，列从0开始数（设计这玩意的人sb吧）
"""

class App:
    def __init__(self,root):
        self.create()
    
    def create(self):
        root.title("Text 示例")
        root.geometry("400x200+400+300")
        
        frame1 = tk.LabelFrame(root,text="文本框信息",padx=10,pady=10,bg="lightblue")
        frame1.pack(pady=20,padx=20,fill="both",expand=True)
        
        self.scroll = tk.Scrollbar(frame1)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.text_area = tk.Text(frame1,width=40,height=8)
        self.text_area.pack(padx=10,pady=10,fill=tk.BOTH,expand=True)
        self.text_area.insert("end","请输入内容...")
        
        self.text_area.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.text_area.yview)
        
        btn = tk.Button(root,text="获取文本",command=self.show_content)
        btn.pack(fill='x',expand=True)
        
        
        menu_bar = tk.Menu(root,tearoff=0)
        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="只读模式",command=lambda:self.disable_text())
        file_menu.add_command(label="正常模式",command=self.enable_text)
        file_menu.add_command(label="清空文本",command=self.clear_text)
        menu_bar.add_cascade(label="编辑",menu=file_menu)
        
        root.config(menu=menu_bar)
    
    def show_content(self):
        content = self.text_area.get("1.0","end")
        # print(f"'{content}'")
        if content != '\n':
            print("你输入了：\n",content)
        else:
            messagebox.showinfo("提示","您未输入任何内容！")
    def clear_text(self):
        self.text_area.delete("1.0",tk.END)
    def disable_text(self):
        self.text_area.config(state="disabled")
    def enable_text(self):
        self.text_area.config(state="normal")

root = tk.Tk()
app =App(root)
root.mainloop()