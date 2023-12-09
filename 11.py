import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QCalendarWidget, QFileDialog, QLabel, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class BirthdayCalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.calendarWidget = QCalendarWidget()
        self.layout.addWidget(self.calendarWidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Дата рождения", "Картинка"])
        self.layout.addWidget(self.tableWidget)

        self.addButton = QPushButton("Добавить человека")
        self.addButton.clicked.connect(self.add_person)
        self.layout.addWidget(self.addButton)

        self.imageLabel = QLabel()
        self.layout.addWidget(self.imageLabel)

        self.chooseImageButton = QPushButton("Выбрать картинку")
        self.chooseImageButton.clicked.connect(self.choose_image)
        self.layout.addWidget(self.chooseImageButton)

    def add_person(self):
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        name, ok = QInputDialog.getText(self, 'Введите имя', 'Имя:')
        if not ok:
            return

        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(name))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(date))

        picture_label = QLabel()
        pixmap = self.imageLabel.pixmap()
        if pixmap:
            picture_label.setPixmap(pixmap)
        self.tableWidget.setCellWidget(row_position, 2, picture_label)

    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать картинку", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaledToWidth(100, Qt.SmoothTransformation)  # Масштабируем изображение до 100 пикселей в ширину
            self.imageLabel.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BirthdayCalendarApp()
    window.setGeometry(100, 100, 600, 400)
    window.show()
    sys.exit(app.exec_())
