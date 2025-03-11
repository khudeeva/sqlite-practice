import sqlite3

# Подключаемся к базе данных
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

#  Удаляем всех пользователей перед вставкой, чтобы избежать дубликатов
cursor.execute("DELETE FROM users")
conn.commit()

# Добавляем пользователей
cursor.execute("INSERT INTO users (name, age) VALUES ('Анна', 22)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Иван', 29)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Мария', 34)")

conn.commit()  # Сохраняем изменения

# Выбираем всех пользователей
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("Список пользователей:")
for user in users:
    print(user)

# Выбираем пользователей, чей возраст больше 30 лет
cursor.execute("SELECT * FROM users WHERE age > 30")
older_users = cursor.fetchall()

print("Пользователи старше 30 лет:")
for user_id, name, age in older_users:
    print(f"ID: {user_id}, Имя: {name}, Возраст: {age}")

# Сортируем пользователей по имени в алфавитном порядке
cursor.execute("SELECT * FROM users ORDER BY name ASC")
sorted_users = cursor.fetchall()

print("Пользователи (отсортированы по имени):")
for user_id, name, age in sorted_users:
    print(f"ID: {user_id}, Имя: {name}, Возраст: {age}")


# Подсчитаем, сколько людей каждого возраста
cursor.execute("SELECT age, COUNT(*) FROM users GROUP BY age")
age_counts = cursor.fetchall()

print("Количество людей каждого возраста:")
for age, count in age_counts:
    print(f"Возраст: {age}, Количество: {count}")


# Закрываем соединение
conn.close()
