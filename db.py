import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='bday.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS birthdays 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                secname TEXT,
                birthday DATE)
        """)

    def create_tables_1(self):
        # Создание таблицы с информацией о событиях
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS events 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Событие TEXT,
                Дата DATE,
                Дней_осталось INTEGER
            )
        ''')

        self.conn.commit()

    def add_birthday(self, data):
        # Вставка данных в базу данных
        self.cur.executemany("INSERT INTO birthdays (name, secname, birthday) VALUES (?, ?, ?)", data)
        self.conn.commit()

    def fetch_data_from_database(self):
        try:
            self.cur.execute('SELECT * FROM birthdays')
            data = self.cur.fetchall()

            return data

        except sqlite3.Error as error:
            print(f"Error while fetching data from the database: {error}")

    def close_connection(self):
        self.conn.close()

    def commit_connection(self):
        self.conn.commit()



# import sqlite3
#
# from datetime import datetime
#
# # Подключение к базе данных SQLite
# conn = sqlite3.connect('bday.db')
# cur = conn.cursor()
#
#
# # Создание таблицы с информацией о днях рождения
# cur.execute("""
#         CREATE TABLE IF NOT EXISTS birthdays
#         (id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         secname TEXT,
#         birthday DATE)
#     """)
#
#     # Создание таблицы с информацией о событиях
# cur.execute('''
#         CREATE TABLE IF NOT EXISTS events (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             Событие TEXT,
#             Дата DATE,
#             Дней осталось INTEGER
#         )
#     ''')
#
# # (first_name, last_name, birthday)
# def add_birthday(peremenay):
#     print(peremenay)
#     # Вставка данных в базу данных
#     cur.executemany("INSERT INTO birthdays (name, secname, birthday) VALUES (?, ?, ?)", peremenay)
#     conn.commit()
#

# def add_event(description, event_date):
#     # Рассчитываем количество дней до события
#     # today = datetime.now().date()
#     # e_date = datetime.strptime(event_date, '%Y-%m-%d').date()
#     # days_left = (e_date - today).days
#
#     # Вставка данных в таблицу events
#     conn = sqlite3.connect('birthdays.db')
#     cur = conn.cursor()
#     cur.execute('INSERT INTO events (description, event_date) VALUES (?, ?)',
#                  (description, event_date))
#     conn.commit()
#     conn.close()

# if __name__ == '__main__':
#     create_tables()

