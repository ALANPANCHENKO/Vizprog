import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, QLineEdit, QCompleter
from PyQt5.QtCore import QSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("YourCompany", "YourApp")  # Set your own values

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.comboBox = QComboBox()
        self.load_items_from_settings()
        self.layout.addWidget(self.comboBox)

        self.lineEdit = QLineEdit()
        self.completer = QCompleter()
        self.lineEdit.setCompleter(self.completer)
        self.layout.addWidget(self.lineEdit)

        self.addButton = QPushButton("Add Item")
        self.addButton.clicked.connect(self.add_item)
        self.layout.addWidget(self.addButton)

        self.clearButton = QPushButton("Clear List")
        self.clearButton.clicked.connect(self.clear_items)
        self.layout.addWidget(self.clearButton)

    def add_item(self):
        new_item_text = self.lineEdit.text()
        if new_item_text:
            self.comboBox.insertItem(0, new_item_text)  # Вставляем новый элемент на первое место
            self.comboBox.setCurrentIndex(0)  # Устанавливаем текущий индекс на новый элемент
            self.lineEdit.clear()
            self.save_items_to_settings()

    def clear_items(self):
        self.comboBox.clear()
        self.save_items_to_settings()

    def load_items_from_settings(self):
        items = self.settings.value("items", [])
        self.comboBox.addItems(items)

    def save_items_to_settings(self):
        items = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
        self.settings.setValue("items", items)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 300, 200)
    window.show()
    sys.exit(app.exec_())
