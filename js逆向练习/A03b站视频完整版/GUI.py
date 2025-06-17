import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import subprocess

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.geometry("600x400+400+300")
        self.root.title("b站视频获取工具")
        self.createData()
        self.createWidgets()
    
    def createData(self):
        self.stateList = ("等待任务...","获取视频中...")
        self.input_url = tk.StringVar()
        self.state = tk.StringVar()
        
        self.cookie = ""
        
        self.state.set(self.stateList[0])
    
    def createWidgets(self):
        frame1 = ttk.Labelframe(self.root,text="信息栏")
        frame1.pack(fill="x",padx=10,pady=5)
        weights = [0,1,0,0]
        for i in range(len(weights)):
            frame1.columnconfigure(i,weight=weights[i])
        
        ttk.Label(frame1,text="输入内容：").grid(row=0,column=0,padx=5,pady=5)
        ttk.Entry(frame1,textvariable=self.input_url).grid(row=0,column=1,padx=5,pady=5,sticky="we")
        ttk.Button(frame1,text="获取视频",command=self.getVideoBtn).grid(row=0,column=2,padx=5,pady=5)
        ttk.Label(frame1,textvariable=self.state).grid(row=1,column=0,padx=5,pady=5)
        # 还需要一个按钮来传入cookie
        ttk.Button(frame1,text="导入cookie",command = self.setCookie).grid(row=0,column=3,padx=5,pady=5)
        
        # 本来想做一个日志信息显示的，犯懒不想做了
    
    def getVideoBtn(self):
        url = self.input_url.get()
        if url:
            choice = messagebox.askokcancel("提示",f"关闭本窗口后开始获取视频：{url}\n时间可能较长，请耐心等待！")
            if choice:
                self.state.set(self.stateList[1])
                self.root.update()
                if not self.cookie:
                    subprocess.run(["python","./video_spider.py",url])
                else:
                    subprocess.run(["python","./video_spider.py",url,self.cookie]) # 这里把cookie设置为每次打开程序的时候输入，保证cookie经常更新
                self.state.set(self.stateList[0])
                self.input_url.set('')
                self.root.update()
            else:
                pass
        else:
            messagebox.showerror("提示","请输入url")
    
    def setCookie(self):
        try:
            self.cookie = self.input_url.get().strip()
            messagebox.showinfo("提示",f"cookie已被设置为：{self.cookie}")
            self.input_url.set('')
        except:
            messagebox.showerror("提示","设置失败，请检查cookie输入是否正确！")

root = tk.Tk()
app = App(root)
root.mainloop()