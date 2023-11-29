import sys
import os
sys.path.append(os.getcwd())
from core.models import db_session
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QComboBox, QMenu, QMessageBox
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor
from gui.form_add_purchase import AddForm
from db.db_control_functions import get_categories, get_products, add_category, \
    get_category_by_name, add_purchase, delete_purcahses
import qdarktheme
from datetime import datetime


def except_hook(cls, exception, traceback):
    """Функция для отлова возможных исключений, вознкающих при работе с Qt"""
    sys.__excepthook__(cls, exception, traceback)
    # TODO: закрывать энджин


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
        self.period_combobox.currentTextChanged.connect(self.update_shown_purchases)
        self.reset_btn.clicked.connect(self.reset_filters)
        self.category_combobox.setInsertPolicy(QComboBox.NoInsert)
        # self.purchase_list.currentCellChanged.connect(self.on_table_context_menu)

        # Вызов предварительных функций
        self.load_all_categories()
        self.load_all_purchases()
        self.calculate_total_cost()
    
    def reload_all_purchases(self):
        """Делает повторнйы запрос в бд на получение покупок"""
        self.all_purchases = get_products(self.session)
        self.update_shown_purchases()
    
    def on_table_context_menu(self):
        """Обработка вызова контекстного меню из таблицы"""
        # selected_rows = 
        print(self.purchase_list.selectionModel().selectedRows())
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.period_combobox.setCurrentIndex(0)
        self.category_combobox.setCurrentIndex(0)
        self.sorting_combobox.setCurrentIndex(0)

    def filter_by_period(self):
        """Оставляет в таблице покупки по фильтру"""
        filtered_purchases = self.get_filtered_purchases(self.all_purchases)
        self.update_shown_purchases(filtered_purchases)
    
    def get_filtered_purchases_by_period(self, purchases: list):
        """Возвращает покупки с фильтром времени"""
        period = self.period_combobox.currentText()
        if not period:
            return purchases
        current_dt = datetime.now()
        dif_days = {"День": 1, "Неделя": 7, "Месяц": 31, "Год": 365}[period]
        return list(filter(lambda x: (current_dt - x.date).days <= dif_days, purchases))
    
    def get_filtered_purchases_by_category(self, purchases: list):
        """Возвращает покупки с фильтром категории"""
        category_name = self.category_combobox.currentText()
        if not category_name: # все категории
            return purchases
        return [i for i in purchases if i.category.name == category_name]

    def load_all_categories(self):
        """Загрузка категорий в меню"""
        self.category_combobox.clear()
        self.category_combobox.addItems([""] + sorted(map(str, self.all_categories)))
    
    def update_shown_purchases(self):
        """Обновляет список показываемых покупок"""
        self.shown_purchases = self.get_filtered_purchases_by_category(
            self.get_filtered_purchases_by_period(self.all_purchases))
        self.calculate_total_cost()
        self.load_all_purchases()
    
    def calculate_total_cost(self):
        """Подсчет суммы потраченных средств за период"""
        value = sum(i.cost for i in self.shown_purchases)
        self.total_cost.setText(str(value))
    
    def load_all_purchases(self):
        """Загрузка покупок в таблицу"""
        self.shown_purchases = self.get_sorted_purchases()
        self.purchase_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.purchase_list.setRowCount(len(self.shown_purchases))
        for i, purchase in enumerate(self.shown_purchases):
            self.purchase_list.setItem(i, 0, QTableWidgetItem(purchase.date.strftime("%d-%m-%Y %H:%M")))
            self.purchase_list.setItem(i, 1, QTableWidgetItem(purchase.name))
            self.purchase_list.setItem(i, 2, QTableWidgetItem(str(purchase.cost)))
            self.purchase_list.setItem(i, 3, QTableWidgetItem(str(purchase.category)))
            self.purchase_list.item(i, 3).setBackground(QColor(purchase.category.color))
    
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
        product_name, cost, category_name, date = args
        print(args)
        date = date.toPyDateTime()
        if category_name not in list(map(str, self.all_categories)): # новая категория
            category = add_category(self.session, category_name)
            self.all_categories.append(category_name)
            self.load_all_categories()
        else:
            category = get_category_by_name(self.session, category_name)
        purchase = add_purchase(self.session, product_name, cost, date, category)
        self.all_purchases.append(purchase)
        self.update_shown_purchases()
    
    def delete_from_table(self, rows):
        """Удаление записей из таблицы"""
        flag = QMessageBox.question(
                self, "Удаление", "Вы уверены, что хотите удлить выбранные записи?"
            )
        if flag != QMessageBox.Yes:
            return
        delete_purcahses(self.session, [self.shown_purchases[i].id for i in rows])
        self.reload_all_purchases()

    def closeEvent(self, _):
        """Ивент закрытия окна"""
        self.session.close()
    
    def contextMenuEvent(self, event):
        """Обработка вызова контекстного меню"""
        selected_rows = self.purchase_list.selectionModel().selectedRows()
        rows = [i.row() for i in selected_rows]
        menu = QMenu()
        if rows:
            menu.addAction("Удалить записи", lambda: self.delete_from_table(rows))
        menu.exec_(self.mapToGlobal(event.pos()))
        
        





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

