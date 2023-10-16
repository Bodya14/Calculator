import sys
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, 
                            QGridLayout, QTextEdit, QMainWindow, QAction, QMenuBar, QColorDialog)
from PyQt5.QtGui import QFont, QIcon

class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История операций")
        self.setGeometry(400, 100, 300, 400)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)
        
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_history)
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(delete_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_history_entry(self, entry):
        self.text_edit.append(entry)
    
    def delete_history(self):
        self.text_edit.clear()

class Calculator(QMainWindow):
    def __init__(self, history_window):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setFixedSize(400, 400)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.result_display = QLineEdit("0")
        self.result_display.setFixedHeight(40)
        self.result_display.setReadOnly(True)

        font = QFont()
        font.setPointSize(16)
        self.result_display.setFont(font)
        
        self.result_display.setStyleSheet(
            "QLineEdit {"
            "   border: 2px solid black;"
            "   border-radius: 5px;"
            "   padding: 5px;"
            "   font-size: 18px;"
            "}"
            "QLineEdit:focus {"
            "   border: 2px solid #0078d7;"
            "}"
        )

        self.layout.addWidget(self.result_display)

        self.buttons = [
            'C', '←', '%', 'π',
            '(', ')', 'x²', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '+/-', '0', '.', '=',
        ]

        self.grid_layout = QGridLayout()

        row = 1
        col = 0

        font = QFont()
        font.setPointSize(14)

        self.current_input = ""
        self.zero_displayed = True
        self.last_input_was_operator = False

        for button_text in self.buttons:
            button = QPushButton(button_text)
            button.setFont(font)
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

            button.clicked.connect(self.button_click)

            button.setStyleSheet(
                "QPushButton {"
                "   background-color: #f0f0f0;"
                "   border: 1px solid #d0d0d0;"
                "   border-radius: 5px;"
                "   padding: 10px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #e0e0e0;"
                "}"
            )

        self.layout.addLayout(self.grid_layout)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.history_window = history_window

    def button_click(self):
        clicked_button = self.sender()
        button_text = clicked_button.text()

        if self.zero_displayed and (button_text.isdigit() or button_text == "."):
            self.result_display.clear()
            self.zero_displayed = False

        if button_text == "=":
            try:
                result = eval(self.current_input.replace(",", "."))
                self.result_display.setText(str(result))
                self.history_window.add_history_entry(f"{self.current_input} = {result}")
                self.current_input = str(result)
            except Exception as e:
                self.result_display.setText("Ошибка")
                self.current_input = ""
        elif button_text == "C":
            self.current_input = ""
            self.result_display.setText("0")
            self.zero_displayed = True
        elif button_text == "←":
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
                if not self.current_input:
                    self.result_display.setText("0")
                    self.zero_displayed = True
                else:
                    self.result_display.setText(self.current_input)
                if self.current_input and not self.current_input[-1].isdigit():
                    self.last_input_was_operator = True
                else:
                    self.last_input_was_operator = False
        elif button_text == "+/-":
            if self.current_input and self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_display.setText(self.current_input)
        elif button_text == "%":
            try:
                result = eval(self.current_input.replace(",", ".")) / 100
                self.result_display.setText(str(result))
                self.current_input = str(result)
            except Exception as e:
                self.result_display.setText("Ошибка")
                self.current_input = ""
                self.zero_displayed = True
        elif button_text in "+-*/":
            if not self.last_input_was_operator:
                self.current_input += button_text
                self.result_display.setText(self.current_input)
                self.last_input_was_operator = True
        elif button_text == "x²":
            try:
                num = eval(self.current_input.replace(",", "."))
                result = num ** 2
                self.result_display.setText(str(result))
                self.history_window.add_history_entry(f"{num}² = {result}")
                self.current_input = str(result)
            except Exception as e:
                self.result_display.setText("Ошибка")
                self.current_input = ""
        elif button_text in "()":
            self.current_input += button_text
            self.result_display.setText(self.current_input)
            self.last_input_was_operator = False
        elif button_text == "π":
            self.current_input += str(math.pi)
            self.result_display.setText(self.current_input)
            self.last_input_was_operator = False
        else:
            self.current_input += button_text
            self.result_display.setText(self.current_input)
            self.last_input_was_operator = False

def change_background_color():
    color = QColorDialog.getColor()
    if color.isValid():
        calc.setStyleSheet(f"QMainWindow{{background-color: {color.name()};}}")

def open_youtube_link():
    import webbrowser
    webbrowser.open("https://youtu.be/GtL1huin9EE?si=11FAntCjiNlvujeN")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('calculate.ico'))

    history_window = HistoryWindow()
    calc = Calculator(history_window)
    calc.show()

    menubar = QMenuBar(calc)
    history_menu = menubar.addMenu("Меню")

    show_history_action = QAction("Показать историю", calc)
    show_history_action.triggered.connect(history_window.show)
    history_menu.addAction(show_history_action)

    change_color_action = QAction("Изменить цвет фона", calc)
    change_color_action.triggered.connect(change_background_color)
    history_menu.addAction(change_color_action)

    help_action = QAction("Справка", calc)
    help_action.triggered.connect(open_youtube_link)
    history_menu.addAction(help_action)

    calc.setMenuBar(menubar)

    sys.exit(app.exec_())
