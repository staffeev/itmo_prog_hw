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


def except_hook(cls, exception, traceback):
    """Функция для отлова возможных исключений, вознкающих при работе с Qt"""
    sys.__excepthook__(cls, exception, traceback)


def wrap_with_session(make_commit=False):
    def __inner_func(func):
        def __inner_inner_func(*args, **kwargs):
            session = db_session.create_session()
            result = func(*args, **kwargs)
            if make_commit:
                session.commit()
            session.close()
            return result
        return __inner_inner_func
    return __inner_func


class MoneyControlApp(QMainWindow):
    """Класс основного окна программы"""
    def __init__(self, path_to_db: str):
        super().__init__()
        loadUi("gui/ui/main_window.ui", self)
        self.setCentralWidget(self.centralwidget)
        self.setLayout(self.gridLayout)
        db_session.global_init(path_to_db)

        self.btn_add_purchase.clicked.connect(self.exec_add_purchase_form)
        self.show_purchases(self.load_purchases())
    
    @staticmethod
    @wrap_with_session()
    def load_purchases() -> list[Purchase]:
        """Возвращает данные о покупках из БД"""
        session = db_session.create_session()
        return session.query(Purchase).all()
    
    @staticmethod
    @wrap_with_session()
    def load_products() -> list[Product]:
        """Возвращает данные о товарах из БД"""
        session = db_session.create_session()
        return session.query(Product).all()

    @staticmethod
    @wrap_with_session()
    def load_categories() -> list[Category]:
        """Возвращает данные о категориях из БД"""
        session = db_session.create_session()
        return session.query(Category).all()
    
    def show_purchases(self, purchases: Purchase):
        """Отображает покупки на виджете с таблицей"""
        print(purchases)
    
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

