import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Application:
    def __init__(self,root):
        self.root = root
        self.createData()
        self.createWidgets()
    
    def createData(self):
        pass
    
    def createWidgets(self):
        frame1 = ttk.Frame(root,relief="sunken",borderwidth=2,padding=10)
        frame1.place(x=0,y=0)
        ttk.Label(frame1,text="show: ",relief="groove").grid(row=0,column=0)
        ttk.Button(frame1,text="click",command=self.EventBtn01).grid(row=0,column=1)
        
        frame2 = ttk.Frame(root,relief="groove",borderwidth=1,padding=10)
        frame2.place(x=200)
        ttk.Label(frame2,text="flat",relief="flat").pack()
        ttk.Label(frame2,text="groove",relief="groove").pack()
        ttk.Label(frame2,text="raised",relief="raised").pack()
        ttk.Label(frame2,text="ridge",relief="ridge").pack()
        ttk.Label(frame2,text="solid",relief="solid").pack()
        ttk.Label(frame2,text="sunken",relief="sunken").pack()
    def EventBtn01(self):
        messagebox.showinfo("提示","This is a message.")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
    