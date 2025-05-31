import tkinter as tk
from tkinter import ttk

"""
Treeview用表格的形式展现数据
常用参数：
columns 列名（逻辑名称）
show="headings" 只显示表头（默认还显示树，左边会多一行）
heading(col,text=...) 设置列标题
column(col,width=...) 设置列宽

.insert(parent, index, values=...) 插入新行，parent=""表示顶层
.delete(item_id) 删除某一行
.item(item_id,values=...) 修改行数据
.selection() 获取选中的项的ID
.get_childrens() 获取所有项
"""

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.create()
        
    def create(self):
        self.root.title("Tree View表格示例")
        tree = ttk.Treeview(self.root,columns=["name","age","gender"],show="headings")
        tree.heading("name",text="姓名")
        tree.heading("age",text="年龄")
        tree.heading("gender",text="性别")
        tree.insert("",tk.END,values=("张三",18,"男"))
        tree.insert("",tk.END,values=("李四",22,"女"))
        

        
        btn = tk.Button(self.root,text="获取选中行",command=lambda t=tree:self.get_selected(t))
        btn.pack()
    
        
        tree.pack(fill='both',expand=True)

    def get_selected(self, tree:ttk.Treeview):
        selected = tree.selection()
        for item in selected:
            values = tree.item(item,"values")
            print("选中数据：",values)

root = tk.Tk()
app = App(root)
root.mainloop()