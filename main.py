import os.path

from PyQt5.QtCore import QDate
from kalendar import *
import sys
import pickle

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

print(os.path.realpath(__file__))
dirname, filename = os.path.split(os.path.realpath(__file__))
print(dirname)

def save_to_file():
    global start_date, time_date , description , dirname
    data_to_save = {"start" : start_date, "end" : time_date, "desc" : description}
    file1 = open(dirname+"\\date.txt", "wb")
    pickle.dump(data_to_save,file1)
    file1.close()
    zadacha = """schtasks /create /tr "python """+os.path.realpath(__file__)+"""" /tn "До наступления события" /sc MINUTE /mo 60 /ed """+time_date.toString("dd/MM/yyyy")+""" /F"""
    print(zadacha)
    os.system('chcp 65001')
    os.system(zadacha)

def read_from_file():
    global start_date, time_date , description , now_date, dirname
    try:
        file1 = open(dirname+"\\date.txt", "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        time_date = data_to_load["end"]
        description = data_to_load["desc"]
        print(start_date.toString('dd-MM-yyyy'),time_date.toString('dd-MM-yyyy'),description)
        ui.calendarWidget.setSelectedDate(time_date)
        ui.dateEdit.setDate(time_date)
        ui.plainTextEdit.setPlainText(description)

        delta_days_left = start_date.daysTo(now_date)     # прошло дней
        delta_days_right = now_date.daysTo(time_date) # осталось дней
        days_total = start_date.daysTo(time_date)       # всего дней

        print(delta_days_left,delta_days_right,days_total)
        procent = int(delta_days_left * 100 / days_total)
        print(procent)
        ui.progressBar.setProperty("value", procent)
    except:
        print("Нет файла")


def on_click():
    global  time_date, description , start_date
    start_date = now_date
    time_date = ui.calendarWidget.selectedDate()
    description = ui.plainTextEdit.toPlainText()
    # print(ui.plainTextEdit.toPlainText())
    # print(ui.dateEdit.dateTime().toString('dd-MM-yyyy'))
    save_to_file()
    # print(ui.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    # date = QDate(2023, 9, 7)
    # ui.calendarWidget.setSelectedDate(date)


def on_click_calendar():
    global start_date, time_date
    # print(ui.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    ui.dateEdit.setDate(ui.calendarWidget.selectedDate())
    time_date = ui.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(time_date)
    # print(delta_days)
    delta_days = start_date.daysTo(time_date)
    ui.label_3.setText("До наступления события: %s дней" % delta_days)

def on_dateedit_change():
    global start_date, time_date
    # print(ui.dateEdit.dateTime().toString('dd-MM-yyyy'))
    ui.calendarWidget.setSelectedDate(ui.dateEdit.date())
    time_date = ui.dateEdit.date()
    delta_days = start_date.daysTo(time_date)
    # print(delta_days)
    ui.label_3.setText("До наступления события: %s дней" %delta_days)


ui.pushButton_2.clicked.connect(on_click) #кнопка отследить
ui.calendarWidget.clicked.connect(on_click_calendar)
ui.dateEdit.dateChanged.connect(on_dateedit_change)


start_date = ui.calendarWidget.selectedDate()
now_date = ui.calendarWidget.selectedDate()
time_date = ui.calendarWidget.selectedDate()
description = ui.plainTextEdit.toPlainText()
read_from_file()
ui.label_4.setText("Сегодняшняя дата: %s " % now_date.toString('dd-MM-yyyy'))
on_click_calendar()

sys.exit(app.exec_())

