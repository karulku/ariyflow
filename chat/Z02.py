import tkinter as tk

class Application:
    def __init__(self, root):
        self.root = root
        self.x=0
        self.y=0
        self.createWidgets()
        
    def createWidgets(self):
        self.label = tk.Label(root,text="移动的标签")
        root.after(100,self.move_label)
    
    def move_label(self):
        print(root.winfo_width(),root.winfo_height(),root.winfo_x(),root.winfo_y())
        self.x+=10
        self.y+=10
        print(self.x,self.y)
        if self.x > root.winfo_width()-100:
            self.x = root.winfo_x()
        if self.y > root.winfo_height()-100:
            self.y = root.winfo_y()
        self.label.place(x=root.winfo_x()+self.x,y=root.winfo_y()+self.y)
        root.after(1000,self.move_label)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()