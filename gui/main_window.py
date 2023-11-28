import sys
import os
sys.path.append(os.getcwd())
from core.models import db_session
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from gui.form_add_purchase import AddForm
from db.db_control_functions import get_categories, get_products, add_category, \
    get_category_by_name, add_purchase


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
        self.session = db_session.create_session()
        # Объявление нужных переменных
        self.all_categories = sorted(get_categories(self.session))
        self.all_purchases = get_products(self.session)
        # Настройка сигналов и слотов
        self.btn_add_purchase.clicked.connect(self.exec_add_purchase_form)
    
    def exec_add_purchase_form(self, _):
        """Метод для работы с формой добавления покупки"""
        form = AddForm()
        if not form.exec():
            return
        self.process_new_purchase(*form.get_data())
        
    def process_new_purchase(self, *args):
        """Обработка данных о новой покупке"""
        product_name, cost, currency_is_usd, category_name, date = args
        date = date.toPyDate()
        if category_name not in self.all_categories: # новая категория
            category = add_category(self.session, category_name)
            self.all_categories.append(category_name)
            self.all_categories.sort()
        else:
            category = get_category_by_name(self.session, category_name)
        purchase = add_purchase(self.session, product_name, cost, currency_is_usd, date, category)

    

    def closeEvent(self, _):
        """Ивент закрытия окна"""
        self.session.close()
        
        





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

