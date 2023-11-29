# def wrap_with_session(func):
#     def __innerr_func(*args, **kwargs):
#         def __inner_inner_func(*args, **kwargs)
#         session = db_session.create



# def f(session):
#     print(f"Hello, session!")


from PyQt5 import QtWidgets
from itertools import product

app = QtWidgets.QApplication([])

# wordlist for testing
wordlist = [''.join(combo) for combo in product('abc', repeat = 4)]

combo = QtWidgets.QComboBox()
combo.addItems(wordlist)

# completers only work for editable combo boxes. QComboBox.NoInsert prevents insertion of the search text
combo.setEditable(True)
combo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

# change completion mode of the default completer from InlineCompletion to PopupCompletion
combo.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

combo.show()
app.exec()