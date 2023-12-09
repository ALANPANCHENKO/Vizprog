import os.path
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QTableWidgetItem

from kalendar import Ui_MainWindow
from db import DatabaseManager
import sys
import pickle

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Инициализация базы данных
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.db_manager.create_tables_1()
        # Инициализация модели для таблицы birthdays
        self.model_birthdays = QSqlTableModel()
        self.model_birthdays.setTable('birthdays')
        self.model_birthdays.select()

        self.model_events = QSqlTableModel()
        self.model_events.setTable('events')
        self.model_events.select()

        # Подключение событий к методам
        self.ui.pushButton_2.clicked.connect(self.on_click)
        self.ui.pushButton_2.clicked.connect(self.populateTableFromDatabase1)
        # self.model_birthdays.select()
        # self.model_events.select()
        self.ui.calendarWidget.clicked.connect(self.on_click_calendar)
        self.ui.dateEdit.dateChanged.connect(self.on_dateedit_change)
        # Заполнение начальных значений
        self.ui.tableWidget.setColumnWidth(0, 104)
        self.ui.tableWidget_2.setColumnWidth(0, 135)
        self.ui.tableWidget_2.setColumnWidth(1, 135)
        self.ui.tableWidget_2.setColumnWidth(2, 134)
        self.start_date = self.ui.calendarWidget.selectedDate()
        self.now_date = self.ui.calendarWidget.selectedDate()
        self.time_date = self.ui.calendarWidget.selectedDate()
        self.description = self.ui.plainTextEdit.toPlainText()
        self.description_1 = self.ui.plainTextEdit_3.toPlainText()
        self.read_from_file()
        self.populateTableFromDatabase1()
        self.populateTableFromDatabase1_1()
        self.ui.label_4.setText("Сегодняшняя дата: %s " % self.now_date.toString('dd-MM-yyyy'))
        self.ui.label_8.setText("Сегодняшняя дата: %s " % self.now_date.toString('dd-MM-yyyy'))
        self.on_click_calendar()

    def populateTableFromDatabase1(self):
        data = self.db_manager.fetch_data_from_database()

        if data:
            self.ui.tableWidget.setRowCount(len(data))
            self.ui.tableWidget.setColumnCount(len(data[0]))

            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.tableWidget.setItem(row_num, col_num, item)

    def populateTableFromDatabase1_1(self):
        data = self.db_manager.fetch_data_from_database_1()

        if data:
            self.ui.tableWidget_2.setRowCount(len(data))
            self.ui.tableWidget_2.setColumnCount(len(data[0]))

            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.tableWidget_2.setItem(row_num, col_num, item)

    # def fill_tableWidget(self):
    #     self.ui.tableWidget.setModel(self.model_birthdays)
    #
    # def fill_tableWidget_2(self):
    #     self.ui.tableWidget_2.setModel(self.model_events)

    def save_to_file(self):
        data_to_save = {"start": self.start_date, "end": self.time_date, "desc": self.description,
                        "Secname": self.description_1}
        file1 = open(os.path.join("date.txt"), "wb")
        pickle.dump(data_to_save, file1)
        file1.close()

    def read_from_file(self):
        try:
            file1 = open(os.path.join("date.txt"), "rb")
            data_to_load = pickle.load(file1)
            file1.close()
            self.start_date = data_to_load["start"]
            self.time_date = data_to_load["end"]
            self.description = data_to_load["desc"]
            self.description_1 = data_to_load["Secname"]
            print(self.start_date.toString('dd-MM-yyyy'), self.time_date.toString('dd-MM-yyyy'),
                    self.description, self.description_1)
            self.ui.calendarWidget.setSelectedDate(self.time_date)
            self.ui.dateEdit.setDate(self.time_date)
            self.ui.plainTextEdit.setPlainText(self.description)
            self.ui.plainTextEdit_3.setPlainText(self.description_1)
            delta_days_left = self.start_date.daysTo(self.now_date)  # прошло дней
            delta_days_right = self.now_date.daysTo(self.time_date)  # осталось дней
            days_total = self.start_date.daysTo(self.time_date)  # всего дней

            procent = int(delta_days_left * 100 / days_total)
            self.ui.progressBar.setProperty("value", procent)
        except FileNotFoundError:
            print("Нет файла")

    def on_click(self):
        self.start_date = self.now_date
        self.time_date = self.ui.calendarWidget.selectedDate()
        self.description = self.ui.plainTextEdit.toPlainText()
        self.description_1 = self.ui.plainTextEdit_3.toPlainText()
        self.left = self.start_date.daysTo(self.time_date)
        people = [(self.description, self.description_1, self.time_date.toString('dd-MM-yyyy'), self.left)]
        self.db_manager.add_birthday(people)
        self.save_to_file()

    def on_click_calendar(self):
        self.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
        self.time_date = self.ui.calendarWidget.selectedDate()
        delta_days = self.start_date.daysTo(self.time_date)
        self.ui.label_3.setText("До наступления события: %s дней" % delta_days)

    def on_dateedit_change(self):
        self.ui.calendarWidget.setSelectedDate(self.ui.dateEdit.date())
        self.time_date = self.ui.dateEdit.date()
        delta_days = self.start_date.daysTo(self.time_date)
        self.ui.label_3.setText("До наступления события: %s дней" % delta_days)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    # main_window.fill_tableWidget()
    # main_window.fill_tableWidget_2()
    sys.exit(app.exec_())
