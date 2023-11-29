import sys
import os
sys.path.append(os.getcwd())
from core.models import db_session
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QComboBox
from PyQt5.uic import loadUi
from gui.form_add_purchase import AddForm
from db.db_control_functions import get_categories, get_products, add_category, \
    get_category_by_name, add_purchase
import qdarktheme


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
        self.all_categories = get_categories(self.session)
        self.all_purchases = get_products(self.session)
        self.shown_purchases = [i for i in self.all_purchases]
        # Настройка сигналов и слотов
        self.purchase_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.btn_add_purchase.clicked.connect(self.exec_add_purchase_form)
        self.sorting_combobox.currentTextChanged.connect(self.load_all_purchases)
        self.category_combobox.currentTextChanged.connect(self.update_shown_purchases)
        self.reset_btn.clicked.connect(self.reset_filters)
        self.category_combobox.setInsertPolicy(QComboBox.NoInsert)

        # Вызов предварительных функций
        self.load_all_categories()
        self.load_all_purchases()
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.period_combobox.setCurrentIndex(0)
        self.category_combobox.setCurrentIndex(0)
        self.sorting_combobox.setCurrentIndex(0)
    

    def load_all_categories(self):
        """Загрузка категорий в меню"""
        self.category_combobox.clear()
        self.category_combobox.addItems([""] + sorted(map(str, self.all_categories)))
    
    def update_shown_purchases(self):
        """Обновляет список показываемых покупок в зависиомсти от выбранной категории"""
        category_name = self.category_combobox.currentText()
        if not category_name: # все категории
            self.shown_purchases = [i for i in self.all_purchases]
        else:
            self.shown_purchases = [i for i in self.all_purchases if i.categories[0].name == category_name]
        self.load_all_purchases()
    
    def load_all_purchases(self):
        """Загрузка покупок в таблицу"""
        sorted_purchases = self.get_sorted_purchases()
        self.purchase_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.purchase_list.setRowCount(len(sorted_purchases))
        for i, purchase in enumerate(sorted_purchases):
            self.purchase_list.setItem(i, 0, QTableWidgetItem(purchase.date.strftime("%d-%m-%Y %H:%M")))
            self.purchase_list.setItem(i, 1, QTableWidgetItem(purchase.name))
            self.purchase_list.setItem(i, 2, QTableWidgetItem(str(purchase.cost)))
            self.purchase_list.setItem(i, 3, QTableWidgetItem(str(purchase.categories[0])))
    
    def get_sorted_purchases(self):
        """Возвращает покупки, отсортированные по ключу из меню"""
        sorting_method = self.sorting_combobox.currentText()
        if sorting_method == "По убыванию даты":
            return sorted(self.shown_purchases, key=lambda x: x.date, reverse=True)
        elif sorting_method == "По возрастанию даты":
            return sorted(self.shown_purchases, key=lambda x: x.date)
        elif sorting_method == "По убыванию цены":
            return sorted(self.shown_purchases, key=lambda x: x.cost, reverse=True)
        elif sorting_method == "По возрастанию цены":
            return sorted(self.shown_purchases, key=lambda x: x.cost)
    
    def exec_add_purchase_form(self, _):
        """Метод для работы с формой добавления покупки"""
        form = AddForm(self.all_categories)
        if not form.exec():
            return
        self.process_new_purchase(*form.get_data())
        
    def process_new_purchase(self, *args):
        """Обработка данных о новой покупке"""
        product_name, cost, currency_is_usd, category_name, date = args
        date = date.toPyDateTime()
        if category_name not in self.all_categories: # новая категория
            category = add_category(self.session, category_name)
            self.all_categories.append(category_name)
            self.load_all_categories()
        else:
            category = get_category_by_name(self.session, category_name)
        purchase = add_purchase(self.session, product_name, cost, currency_is_usd, date, category)
        self.all_purchases.append(purchase)
        self.update_shown_purchases()
    

    def closeEvent(self, _):
        """Ивент закрытия окна"""
        self.session.close()
        
        





def run_app(path_to_db: str):
    """Запуск программы"""
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    # app.setStyle('fusion')
    programm = MoneyControlApp(path_to_db)
    programm.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
    

if __name__ == "__main__":
    run_app("db/purchases.db")

