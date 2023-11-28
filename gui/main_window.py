import sys
import os
sys.path.append(os.getcwd())
from core.models import db_session
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from core.models.purchase import Purchase
from core.models.product import Product
from core.models.category import Category
from gui.form_add_purchase import AddForm
from db.db_control_functions import *


def except_hook(cls, exception, traceback):
    """Функция для отлова возможных исключений, вознкающих при работе с Qt"""
    sys.__excepthook__(cls, exception, traceback)


class MoneyControlApp(QMainWindow):
    """Класс основного окна программы"""
    def __init__(self, path_to_db: str):
        super().__init__()
        loadUi("gui/ui/main_window.ui", self)
        self.setCentralWidget(self.centralwidget)
        self.setLayout(self.gridLayout)
        db_session.global_init(path_to_db)
        self.btn_add_purchase.clicked.connect(self.exec_add_purchase_form)
    
    def exec_add_purchase_form(self, _):
        """Метод для работы с формой добавления покупки"""
        form = AddForm()
        if not form.exec():
            return




def run_app(path_to_db: str):
    """Запуск программы"""
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    programm = MoneyControlApp(path_to_db)
    programm.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
    

if __name__ == "__main__":
    run_app("db/purchases.db")

