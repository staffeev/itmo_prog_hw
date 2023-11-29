from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QComboBox
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi


class AddForm(QDialog):
    """Класс формы для добавления покупки"""
    def __init__(self, categories: list[str]):
        super().__init__()
        loadUi("gui/ui/add_purchase_form.ui", self)
        self.setLayout(self.gridLayout)
        self.category_choice.addItems(sorted(map(str, categories)))
        self.category_choice.setInsertPolicy(QComboBox.NoInsert)
        self.calendar.setDateTime(QDateTime.currentDateTime())
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

    def get_data(self):
        """Возвращает данные из формы"""
        product_name = self.product_name.text()
        cost = self.cost_spinbox.value()
        category_name = self.category_choice.currentText()
        date = self.calendar.dateTime()
        return product_name, cost, category_name, date
    
    def accept(self):
        """Проверка корректности введенных данных"""
        product_name = self.product_name.text()
        category = self.category_choice.currentText()
        if not product_name and not category:
            QMessageBox.critical(self, "Ошибка", "Название товара и категория отсутствуют")
            return
        elif not product_name:
            QMessageBox.critical(self, "Ошибка", "Название товара отсутствует")
            return
        elif not category:
            QMessageBox.critical(self, "Ошибка", "Категоия товара не выбрана")
            return
        self.done(1)
