import tkinter as tk
from tkinter import messagebox

""" 
Text中的undo参数设置text中的内容可以撤销和重做
pack中的expand参数表示该组件是否参与额外空间分配
"""
""" cursor用于设置悬停时的鼠标图标，arrow表示箭头图标 """
class SimpleNotepad:
    def __init__(self, root):
        self.root = root
        self.text_area = tk.Text(root,undo=True, font=("Arial",12))
        self.text_area.pack(fill="both",expand=True)
        
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side="right",fill="y")
        """ 这两条绑定下拉栏和text，必须一起用 """
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        """ cursor设置鼠标悬浮在上面的时候显示什么，arrow就是鼠标箭头 """
        self.scrollbar.config(cursor="arrow") 
        self.file_path = None
        self.createMenu()
    
    def createMenu(self):
        menu_bar = tk.Menu(self.root)
        """ tearoff为1时菜单栏可以撕裂下来变成一个独立窗口，为0时不行 """
        
        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="打开",command = self.open_file)
        file_menu.add_command(label="保存",command=self.save_file)
        file_menu.add_command(label="另存为",command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="退出",command=self.quit)
        menu_bar.add_cascade(label="文件",menu=file_menu)
        
        # 编辑菜单
        edit_menu = tk.Menu(menu_bar,tearoff=0)
        edit_menu.add_command(label="撤销",command=self.text_area.edit_undo)
        edit_menu.add_command(label="重做",command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="剪切",command=lambda: root.focus_get().event_generate("<<Cut>>"))
        
        root.config(menu=menu_bar)
    
    def open_file(self):
        pass
    
    def save_file(self):
        pass
    
    def save_as(self):
        pass
    
    def quit(self):
        pass
        
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("简易记事本")
    root.geometry("600x400+400+300")
    app = SimpleNotepad(root)
    root.mainloop()