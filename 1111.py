import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit, QWidget


class TableSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Создаем таблицу
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Имя', 'Фамилия', 'Возраст'])

        # Заполняем таблицу данными
        self.populateTable()

        # Создаем поле для ввода текста поиска
        self.search_line_edit = QLineEdit(self)
        self.search_line_edit.setPlaceholderText('Введите текст для поиска')
        self.search_line_edit.textChanged.connect(self.filterTable)

        # Добавляем виджеты в основной макет
        self.layout.addWidget(self.search_line_edit)
        self.layout.addWidget(self.table)

        # Устанавливаем макет в центральный виджет
        self.central_widget.setLayout(self.layout)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Поиск по таблице в PyQt5')
        self.show()

    def populateTable(self):
        # Пример данных для таблицы
        data = [
            ('Иван', 'Иванов', '25'),
            ('Петр', 'Петров', '30'),
            ('Анна', 'Сидорова', '22'),
            ('Мария', 'Кузнецова', '35'),
        ]

        # Заполняем таблицу данными
        self.table.setRowCount(len(data))
        for row, (name, surname, age) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(surname))
            self.table.setItem(row, 2, QTableWidgetItem(age))

    def filterTable(self):
        # Получаем текст из поля поиска
        filter_text = self.search_line_edit.text().lower()

        # Проходим по всем строкам таблицы и скрываем те, которые не соответствуют поисковому тексту
        for row in range(self.table.rowCount()):
            row_text = ' '.join([self.table.item(row, col).text().lower() for col in range(self.table.columnCount())])
            if filter_text in row_text:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableSearchApp()
    sys.exit(app.exec_())
