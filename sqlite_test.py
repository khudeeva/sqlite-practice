import sqlite3

# Подключаемся к базе данных (файл test.db создастся автоматически)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Создаём таблицу пользователей (если её нет)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

print("База данных `test.db` успешно создана и готова к работе!")

# Закрываем соединение
conn.close()
