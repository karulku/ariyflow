import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        
        self.root.title("颜色调节面板")
        self.root.geometry("500x400+400+300")
        self.createData()
        self.create()
    
    def createData(self):
        self.R = tk.IntVar()
        self.G = tk.IntVar()
        self.B = tk.IntVar()
        self.R.set(255)
        self.G.set(255)
        self.B.set(255)
    def create(self):
        frame1 = tk.LabelFrame(self.root,bg="lightblue",text="颜色设置",padx=10,pady=5)
        frame1.pack(fill='both',expand=True,padx=10,pady=5)
        frame1.columnconfigure(1,weight=1)
        tk.Label(frame1,text="红色：").grid(row=0,column=0,pady=5)
        tk.Scale(frame1,orient=tk.HORIZONTAL,variable=self.R,command=lambda x:self.change_color(),from_=0,to=255).grid(row=0,column=1,sticky="we",pady=5)
        
        tk.Label(frame1,text="绿色：").grid(row=1,column=0)
        tk.Scale(frame1,variable=self.G,orient=tk.HORIZONTAL,command=lambda x:self.change_color(),from_=0,to=255).grid(row=1,column=1,sticky="we",pady=5)
        
        tk.Label(frame1,text="蓝色：").grid(row=2,column=0)
        tk.Scale(frame1,orient="horizontal",variable=self.B,command=lambda x:self.change_color(),from_=0,to=255).grid(row=2,column=1,sticky="we",pady=5)
        
        frame2 = tk.Frame(self.root,height=60)
        frame2.pack(fill="both",expand=True)
        self.color_label = tk.Label(frame2,text="颜色预览")
        self.color_label.pack(fill='both',expand=True)
        
        frame3 = tk.Frame(self.root,bg="lightgreen")
        frame3.pack(fill="both",expand=True)
        weights = [1,0,0,1]
        for i in range(len(weights)):
            frame3.columnconfigure(i,weight=weights[i])
        tk.Button(frame3,text="重置",command=lambda:self.reset(),relief="groove",width=6,height=1).grid(row=0,column=1,padx=10,pady=10)
        tk.Button(frame3,text="提交",command=lambda:self.submit(),relief="groove",width=6,height=1).grid(row=0,column=2,padx=10,pady=10)
        
    
    def change_color(self):
        color = self.R.get().to_bytes()+self.G.get().to_bytes()+self.B.get().to_bytes()
        # print(color.hex())
        self.color_label.config(bg=f"#{color.hex()}")
    
    def reset(self):
        self.R.set(255)
        self.G.set(255)
        self.B.set(255)
    def submit(self):
        messagebox.showinfo("提示",f"红色：{self.R.get()}\n绿色：{self.G.get()}\n蓝色：{self.B.get()}")
        self.reset()

root = tk.Tk()
app = App(root)
root.mainloop()