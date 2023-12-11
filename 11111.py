import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sqlite3
from datetime import datetime
from PyQt5.QtCore import Qt  # Добавим импорт класса Qt

class EventManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных
        self.initDB()

        # Инициализация пользовательского интерфейса
        self.initUI()

    def initDB(self):
        # Подключение к базе данных SQLite
        self.conn = sqlite3.connect('events.db')
        self.cursor = self.conn.cursor()

        # Создание таблицы events, если её нет
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                description TEXT,
                date TEXT,
                image BLOB
            )
        ''')
        self.conn.commit()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Создание таблицы
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Событие', 'Описание', 'Дата', 'Изображение'])

        # Создание виджетов для ввода данных
        self.event_line_edit = QLineEdit(self)
        self.description_line_edit = QLineEdit(self)
        self.date_line_edit = QLineEdit(self)
        self.image_label = QLabel('Изображение:', self)
        self.browse_button = QPushButton('Обзор', self)
        self.browse_button.clicked.connect(self.browseImage)

        # Создание кнопки добавления события
        self.add_event_button = QPushButton('Добавить событие', self)
        self.add_event_button.clicked.connect(self.insertEvent)

        # Добавление виджетов в основной макет
        self.layout.addWidget(self.event_line_edit)
        self.layout.addWidget(self.description_line_edit)
        self.layout.addWidget(self.date_line_edit)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.add_event_button)
        self.layout.addWidget(self.table)

        # Установка макета в центральный виджет
        self.central_widget.setLayout(self.layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Менеджер событий')
        self.show()

    def browseImage(self):
        # Диалоговое окно для выбора изображения
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Images (*.png *.jpg *.bmp)')

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "rb") as image_file:
                    self.image_data = image_file.read()

                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaledToWidth(100)
                self.image_label.setPixmap(pixmap)
                self.image_label.setAlignment(Qt.AlignCenter)  # Используем Qt.AlignCenter вместо целого числа

            except Exception as e:
                print(f"Ошибка при загрузке изображения: {e}")

    def insertEvent(self):
        event = self.event_line_edit.text()
        description = self.description_line_edit.text()
        date = self.date_line_edit.text()

        try:
            # Проверка формата даты
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print('Неверный формат даты. Используйте ГГГГ-ММ-ДД.')
            return
        print(self.image_data)
        # Вставка данных в базу данных
        self.cursor.execute('''
            INSERT INTO events (event, description, date, image)
            VALUES (?, ?, ?, ?)
        ''', (event, description, date, self.image_data))
        self.conn.commit()

        # Обновление таблицы
        self.populateTable()

    def populateTable(self):
        # Очистка таблицы
        self.table.setRowCount(0)

        # Получение данных из базы данных и добавление их в таблицу
        self.cursor.execute('SELECT * FROM events')
        data = self.cursor.fetchall()

        for row, (event_id, event, description, date, image) in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(event))
            self.table.setItem(row, 1, QTableWidgetItem(description))
            self.table.setItem(row, 2, QTableWidgetItem(date))

            # Отображение изображения
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToWidth(100)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)  # Используем Qt.AlignCenter
            self.table.setCellWidget(row, 3, image_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EventManagerApp()
    sys.exit(app.exec_())
