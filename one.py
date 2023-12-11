import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QLabel
from PyQt5.QtGui import QPixmap


class DatabaseManager:
    def __init__(self, db_name='bday.db'):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_name)

        if not self.db.open():
            print(f"Error: {self.db.lastError().text()}")

        self.create_tables()

    def create_tables(self):
        query = QtSql.QSqlQuery()
        query.exec_("""
            CREATE TABLE IF NOT EXISTS birthdays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                secname TEXT,
                birthday DATE,
                left_days INTEGER,
                picture BLOB
            )
        """)

    def add_birthday(self, name, secname, birthday, left_days, picture=None):
        query = QtSql.QSqlQuery()
        query.prepare("""
            INSERT INTO birthdays (name, secname, birthday, left_days, picture)
            VALUES (?, ?, ?, ?, ?)
        """)

        query.addBindValue(name)
        query.addBindValue(secname)
        query.addBindValue(birthday)
        query.addBindValue(left_days)
        query.addBindValue(picture)

        if not query.exec_():
            print(f"Error: {query.lastError().text()}")

    def fetch_all_birthdays(self):
        query = QtSql.QSqlQuery("SELECT * FROM birthdays")
        birthdays = []

        while query.next():
            id = query.value(0)
            name = query.value(1)
            secname = query.value(2)
            birthday = query.value(3)
            left_days = query.value(4)
            picture = query.value(5)

            birthdays.append({
                'id': id,
                'name': name,
                'secname': secname,
                'birthday': birthday,
                'left_days': left_days,
                'picture': picture,
            })

        return birthdays

    def delete_birthday_by_id(self, birthday_id):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM birthdays WHERE id = ?")
        query.addBindValue(birthday_id)

        if not query.exec_():
            print(f"Error: {query.lastError().text()}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(6)  # Добавляем столбец для изображения
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Name', 'Secname', 'Birthday', 'Left Days', 'Picture'])

        add_button = QtWidgets.QPushButton('Add Birthday', self)
        add_button.clicked.connect(self.add_birthday)

        delete_button = QtWidgets.QPushButton('Delete Selected', self)
        delete_button.clicked.connect(self.delete_selected_birthday)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.populate_table()

    def populate_table(self):
        self.tableWidget.setRowCount(0)

        birthdays = self.db_manager.fetch_all_birthdays()
        for row, birthday in enumerate(birthdays):
            self.tableWidget.insertRow(row)
            for col, (key, value) in enumerate(birthday.items()):
                if col == 5:  # Обработка столбца с изображением
                    image_label = QLabel()
                    pixmap = QPixmap()
                    pixmap.loadFromData(value)
                    pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                    image_label.setAlignment(Qt.AlignCenter)
                    self.tableWidget.setCellWidget(row, col, image_label)
                else:
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)

    def add_birthday(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Input', 'Enter Name:')
        if ok:
            secname, ok = QtWidgets.QInputDialog.getText(self, 'Input', 'Enter Secname:')
            if ok:
                birthday, ok = QtWidgets.QInputDialog.getText(self, 'Input', 'Enter Birthday (YYYY-MM-DD):')
                if ok:
                    left_days, ok = QtWidgets.QInputDialog.getInt(self, 'Input', 'Enter Left Days:')
                    if ok:
                        picture_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Picture', '', 'Images (*.png *.jpg *.bmp)')
                        if picture_path:
                            with open(picture_path, 'rb') as file:
                                picture_data = file.read()
                            self.db_manager.add_birthday(name, secname, birthday, left_days, picture_data)
                            self.populate_table()

    def delete_selected_birthday(self):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:
            birthday_id = int(self.tableWidget.item(current_row, 0).text())
            self.db_manager.delete_birthday_by_id(birthday_id)
            self.populate_table()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
