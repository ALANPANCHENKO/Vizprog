import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate
import sqlite3

class BirthdayApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных
        self.init_db()

        # Инициализация пользовательского интерфейса
        self.init_ui()

    def init_db(self):
        # Подключение к базе данных SQLite
        self.conn = sqlite3.connect('birthdays.db')
        self.cur = self.conn.cursor()

        # Создание таблицы, если она не существует
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS birthdays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                birthday DATE
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Виджеты ввода данных
        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.birthday_input = QLineEdit(self)
        self.add_button = QPushButton('Добавить', self)
        self.calculate_days_button = QPushButton('Рассчитать дни', self)

        # Таблица для отображения данных
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'День рождения'])

        # Размещение виджетов на форме
        self.layout.addWidget(QLabel('Имя:'))
        self.layout.addWidget(self.first_name_input)
        self.layout.addWidget(QLabel('Фамилия:'))
        self.layout.addWidget(self.last_name_input)
        self.layout.addWidget(QLabel('День рождения (ГГГГ-ММ-ДД):'))
        self.layout.addWidget(self.birthday_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.calculate_days_button)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        # Подключение слотов и сигналов
        self.add_button.clicked.connect(self.add_birthday)
        self.calculate_days_button.clicked.connect(self.calculate_days)

        # Загрузка данных из базы в таблицу
        self.load_data()

    def add_birthday(self):
        # Получение данных из виджетов ввода
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        birthday = self.birthday_input.text()

        # Вставка данных в базу данных
        self.cur.execute('INSERT INTO birthdays (first_name, last_name, birthday) VALUES (?, ?, ?)',
                         (first_name, last_name, birthday))
        self.conn.commit()

        # Очистка полей ввода
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.birthday_input.clear()

        # Обновление данных в таблице
        self.load_data()

    def calculate_days(self):
        # Рассчитываем количество дней до дня рождения
        today = QDate.currentDate()
        self.cur.execute('SELECT id, first_name, last_name, birthday FROM birthdays')
        data = self.cur.fetchall()

        for row in data:
            id, first_name, last_name, birthday = row
            b_date = QDate.fromString(birthday, 'yyyy-MM-dd')
            days_left = today.daysTo(b_date)

            # Обновление ячейки с количеством дней
            self.cur.execute('UPDATE birthdays SET days_left = ? WHERE id = ?', (days_left, id))
            self.conn.commit()

        # Обновление данных в таблице
        self.load_data()

    def load_data(self):
        # Загружаем данные из базы данных в таблицу
        self.table.setRowCount(0)
        self.cur.execute('SELECT id, first_name, last_name, birthday FROM birthdays')
        data = self.cur.fetchall()

        for row_index, row_data in enumerate(data):
            self.table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_index, col_index, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BirthdayApp()
    window.setWindowTitle('База данных дней рождения')
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
