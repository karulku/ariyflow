import tkinter as tk
from tkinter import messagebox
# 注意学习一下函数传参的方式
class Calculator:
    def __init__(self, root):
        self.root = root
        
        self.createData()
        self.createWidgets()
        
    def createData(self):
        self.entryVar = tk.StringVar()
    
    def createWidgets(self):
        frame1 = tk.Frame(root,borderwidth=2,relief="sunken")
        frame1.place(x=0,y=0)
        
        tk.Entry(frame1,textvariable=self.entryVar,relief="sunken",width=40).pack(fill="x")
        frame2 = tk.Frame(frame1,borderwidth=1,relief="sunken")
        frame2.pack()
        btns = [
            ('7','8','9','/'),
            ('4','5','6','*'),
            ('1','2','3','-'),
            ('0','.','=','+')
        ]
        for i,row in enumerate(btns):
            for j,ch in enumerate(row):
                tk.Button(frame2,borderwidth=2,relief="ridge",text=ch,command=lambda ch=ch:self.click_btn(ch),width=8).grid(row=i,column=j,pady=1,padx=1)
        
        tk.Button(frame2,text="清空",command=self.clear,relief="ridge",borderwidth=2,padx=1,pady=1,width=18).grid(row=4,column=0,columnspan=2)
        tk.Button(frame2,text="删除",command=self.backspace,relief="ridge",borderwidth=2,padx=1,pady=1,width=18).grid(row=4,column=2,columnspan=2)
    
    def click_btn(self,ch: str):
        if ch == "=":
            try:
                ans = eval(self.entryVar.get())
                self.entryVar.set(ans)
            except:
                messagebox.showerror("提示","未知错误！")
                return
        else:
            self.entryVar.set(self.entryVar.get()+ch)
    
    def clear(self):
        self.entryVar.set('')
    
    def backspace(self):
        self.entryVar.set(self.entryVar.get()[:-1])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("290x300+400+300")
    root.title("计算器")
    app = Calculator(root)
    root.mainloop()