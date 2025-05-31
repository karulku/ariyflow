import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        # 显示框
        self.input_frame = tk.Frame(root)
        self.input_frame.pack()

        self.input_field = tk.Entry(
            self.input_frame, textvariable=self.input_text,
            font=('Arial', 18), width=25, bd=8, relief='ridge', justify='right'
        )
        self.input_field.grid(row=0, column=0, ipady=10)

        # 按钮框
        self.btns_frame = tk.Frame(root)
        self.btns_frame.pack()

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                button = tk.Button(
                    self.btns_frame, text=char, width=9, height=3,
                    font=('Arial', 14), command=lambda ch=char: self.on_button_click(ch)
                )
                button.grid(row=r, column=c)

        # 清除按钮
        clear_btn = tk.Button(
            self.root, text='清除', width=40, height=2,
            font=('Arial', 12), command=self.clear_input
        )
        clear_btn.pack(pady=5)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = str(eval(self.expression))
                self.input_text.set(result)
                self.expression = result
            except Exception:
                self.input_text.set("错误")
                self.expression = ""
        else:
            self.expression += str(char)
            self.input_text.set(self.expression)

    def clear_input(self):
        self.expression = ""
        self.input_text.set("")


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
