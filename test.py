import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class ComboBoxWithCheckBoxes(QComboBox):
    """Класс выпадающего списка значений с возможностью отметить несколько
    значений"""
    def __init__(self, names=None):
        """Функция-инициализатор"""
        super().__init__()
        self.changed_value = False
        if names is not None:
            self.names = names
        self.view().pressed.connect(self.press_item)

    def hidePopup(self):
        """Функция, которая будет прятать выпадающий список или
        оставлять открытым"""
        if not self.changed_value:
            super().hidePopup()
        self.changed_value = False

    def if_item_checked(self, i):
        """Функция, возвращающая истину, если элемент с некоторым индексом
        отмечен, иначе ложь"""
        item = self.model().item(i, self.modelColumn())
        if item is not None:
            return item.checkState() == Qt.Checked

    def press_item(self, i):
        """Функция замены отметки на ее отсутствие у элемента или наоборот"""
        item = self.model().itemFromIndex(i)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            if item.text() == 'Все':
                for x in range(1, self.count()):
                    it = self.model().item(x, self.modelColumn())
                    it.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
            if item.text() == 'Все':
                for x in range(1, self.count()):
                    it = self.model().item(x, self.modelColumn())
                    it.setCheckState(Qt.Checked)
        self.changed_value = True

    def check_item(self, i):
        """Функция для создания отметки у элемента (пустой)"""
        new_item = self.model().item(i, self.modelColumn())
        new_item.setCheckState(Qt.Unchecked)


class CheckableComboBox(QComboBox):
	def __init__(self):
		super().__init__()
		self._changed = False

		self.view().pressed.connect(self.handleItemPressed)

	def setItemChecked(self, index, checked=False):
		item = self.model().item(index, self.modelColumn()) # QStandardItem object

		if checked:
			item.setCheckState(Qt.Checked)
		else:
			item.setCheckState(Qt.Unchecked)

	def handleItemPressed(self, index):
		item = self.model().itemFromIndex(index)

		if item.checkState() == Qt.Checked:
			item.setCheckState(Qt.Unchecked)
		else:
			item.setCheckState(Qt.Checked)
		self._changed = True


	def hidePopup(self):
		if not self._changed:
			super().hidePopup()
		self._changed = False

	def itemChecked(self, index):
		item = self.model().item(index, self.modelColumn())
		return item.checkState() == Qt.Checked

class MyApp(QWidget):
	def __init__(self):
		super().__init__()
		self.resize(500, 150)

		mainLayout = QVBoxLayout()

		self.combo = CheckableComboBox()
		self.combo2 = ComboBoxWithCheckBoxes()
		mainLayout.addWidget(self.combo)
		mainLayout.addWidget(self.combo2)

		for i in range(6):
			self.combo.addItem('Item {0}'.format(str(i)))
			self.combo.setItemChecked(i, False)
			self.combo2.addItem('Item {0}'.format(str(i)))
			self.combo2.check_item(i)
		
		btn = QPushButton('Print Values')
		btn.clicked.connect(self.getValue)
		mainLayout.addWidget(btn)

		self.setLayout(mainLayout)

	def getValue(self):
		for i in range(self.combo.count()):
			print('Index: {0} is checked {1}'.format(i, self.combo.itemChecked(i)))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			font-size: 40px;
		}
	''')

	myApp = MyApp()
	myApp.show()

	app.exit(app.exec_())	