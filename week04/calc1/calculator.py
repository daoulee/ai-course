import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("나의 계산기")
        self.root.geometry("300x400")

        self.result_var = tk.StringVar()

        # 입력창 생성
        self.entry = tk.Entry(root, textvariable=self.result_var, font=("Arial", 24), bd=10, insertwidth=4, width=14, borderwidth=4, justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, pady=20)

        # 버튼 구성
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.on_click(x)
            tk.Button(root, text=button, width=5, height=2, font=("Arial", 14),
                      command=action).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_click(self, char):
        if char == '=':
            try:
                # eval 함수를 사용하여 문자열 계산식 실행
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except ZeroDivisionError:
                messagebox.showerror("에러", "0으로 나눌 수 없습니다.")
                self.result_var.set("")
            except Exception:
                messagebox.showerror("에러", "잘못된 수식입니다.")
                self.result_var.set("")
        elif char == 'C':
            self.result_var.set("")
        else:
            current_text = self.result_var.get()
            self.result_var.set(current_text + char)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
