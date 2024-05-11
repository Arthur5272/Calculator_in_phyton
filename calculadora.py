import tkinter as tk
import re
from typing import List

class Calculadora:

    def __init__(
        self,
        root: tk.Tk,
        label: tk.Label,
        display: tk.Entry,
        buttons: List[List[tk.Button]]
    ) -> None:
        self.root = root
        self.label = label
        self.display = display
        self.buttons = buttons

    def start(self):
        self._config_buttons()
        self.root.mainloop()

    def _config_buttons(self):
        buttons = self.buttons
        for row_values in buttons:
            for button in row_values:
                button_text = button["text"]

                if button_text == "C":
                    button.bind("<Button-1>", self.clear)
                    button.config(bg="#CF0B0B", foreground="#fff")

                if button_text in ".+-*/()^":
                    button.bind("<Button-1>", self.add_text_to_display)
                    button.config(bg="#424242", foreground="#fff")

                if button_text in "0123456789":
                    button.bind("<Button-1>", self.add_text_to_display)
                    button.config(bg="#3E314F", foreground="#fff")

                if button_text == "=":
                    button.bind("<Button-1>", self.calculate)
                    button.config(bg="#17CF54", foreground="#fff")

    def _fix_text(self, text):
        # Substitui tudo que náo for números e simbolos
        text = re.sub(r'[^\d\.\/\*\+\-\^\(\)e]', r'', text, 0)
        # Substitui operadores repetidos
        text = re.sub(r'([\.\+\/\-\*\^])\1+',r'\1', text, 0)
        # Substitui parenteses sem conteudo para nada
        text = re.sub(r'\*?\(\)', '', text)
        return text

    def add_text_to_display(self, event=None):
        self.display.insert("end", event.widget["text"])

    def calculate(self, event=None):
        fixed_text = self._fix_text(self.display.get())
        equations = self._get_equations(fixed_text)
        
        try:
            if len(equations) == 1:
                result = eval(self._fix_text(equations[0]))
                
            else:
                transform = eval(self._fix_text(equations[0]))
                result = pow(transform, eval(self._fix_text(equations[1])))
                
            self.clear()
            self.display.insert("end", result)
            self.label.config(text=f'{fixed_text} = {result}')
            tx = f'{fixed_text} = {result}\n'
            o = open("historico.txt", "a")
            o.write(tx)
            o.close()
            
        except OverflowError:
            self.label.config(text="Náo foi possivel realizar essa equacão, simplifique.")
        except Exception:
            self.label.config(text="Equacão invalida")

    def _get_equations(self, text):
        return re.split(r'\^', text, 0)

    def clear(self, event=None):
        self.display.delete(0, "end")

def make_root() -> tk.Tk:
    root = tk.Tk()
    root.title("Cálculadora")
    root.config(padx=10, pady=10, bg="#2C2C2C")
    root. resizable(False, False) 
    return root

def make_label(root) -> tk.Label:
    label = tk.Label(
        root, text="Nenhuma operação realizada",
        anchor="e", justify="right", bg="#2C2C2C", foreground="#fff"
    )
    label.grid(row=0, column=0, columnspan=5, sticky="news")
    return label

def make_display(root) -> tk.Entry:
    display = tk.Entry(root)
    display.grid(row=1, column=0, columnspan=5, sticky="news", pady=(0, 10))
    display.config(
        font=("Times New Roman", 40, "bold"),
        justify="right", bd=1, relief="flat",
        highlightthickness=1, highlightcolor="#ccc", bg="#424242", foreground="#fff"
    )
    display.bind("<Control-a>", display_control_a)
    return display

def display_control_a(event):
    event.widget.select_range(0, "end")
    event.widegt.incursor("end")
    return "break"

def make_buttons(root) -> List[List[tk.Button]]:
    button_texts: list[list[str]] = [
        ['7', '8', '9', '+', 'C'],
        ['4', '5', '6', '-', '*'],
        ['1', '2', '3', '/', '^'],
        ['.', '0', '(', ')', '='],
    ]

    buttons: list[List[tk.Button]] = []

    for row, row_value in enumerate(button_texts, start=2):
        button_row = []
        for col_index, col_value in enumerate(row_value):
            btn = tk.Button(root, text=col_value)
            btn.grid(row=row, column=col_index, sticky='news', padx=5, pady=5)
            btn.config(
                font=("Times New Roman", 15, "normal"),
                pady=40, width=1, bg="#f1f2f3", bd=0,
                cursor="hand2", highlightthickness=0, highlightcolor="#ccc",
                activebackground="#ccc", highlightbackground="#ccc"
            )
            button_row.append(btn)
        buttons.append(button_row)
    return buttons

def main():
    root = make_root()
    display = make_display(root)
    label = make_label(root)
    buttons = make_buttons(root)
    calculadora = Calculadora(root, label, display, buttons)
    calculadora.start()

if __name__ == '__main__':
    main()