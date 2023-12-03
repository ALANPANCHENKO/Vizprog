import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel

class DatabaseManager:
    def __init__(self, db_name='bday.db'):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_name)
        if not self.db.open():
            print("Не удалось подключиться к базе данных")

    def close_connection(self):
        self.db.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Пример работы с базой данных и таблицей')

        # Создаем QSqlQueryModel
        self.query_model = QSqlQueryModel()

        # Устанавливаем запрос для выборки данных из таблицы birthdays
        self.query_model.setQuery("SELECT * FROM birthdays")

        # Создаем QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.query_model)

        # Создаем основной макет
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        # Создаем виджет и устанавливаем основной макет
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Устанавливаем виджет в качестве центрального виджета главного окна
        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        # Закрываем соединение с базой данных при закрытии главного окна
        self.db_manager.close_connection()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
