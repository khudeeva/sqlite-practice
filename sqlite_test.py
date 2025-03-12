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

# Создаем таблицу jobs (если её нет)
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    job_title TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

print(f"Таблица 'jobs' успешно создана!")


#  Удаляем старые данные перед вставкой, чтобы избежать дубликатов
cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM jobs")
conn.commit()

# Добавляем пользователей
users_data = [
    ("Анна", 22),
    ("Иван", 29),
    ("Мария", 34),
    ("Алексей", 29),
    ("Светлана", 22)
]

cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users_data)
conn.commit()  # Сохраняем изменения()

# Получаем ID пользователей
cursor.execute("SELECT id, name FROM users")
users = cursor.fetchall()

# Создаем список профессий, зная id пользователя
jobs_data = [
    (users[0][0], "Разработчик"),
    (users[1][0], "Тестировщик"),
    (users[2][0], "Маркетолог"),
    (users[3][0], "Дизайнер"),
    (users[4][0], "Аналитик")
]

# Добавляем профессиии
cursor.executemany("INSERT INTO jobs (user_id, job_title) VALUES (?, ?)", jobs_data)
conn.commit()

print("Данные о профессиях добавлены в 'jobs'!")

# Выполняем объединение таблиц 'users' и 'jobs' с 'JOIN'
cursor.execute('''
SELECT users.name, users.age, jobs.job_title
FROM users
LEFT JOIN jobs ON users.id = jobs.user_id
''')

print("Список пользоватлей и их профессий:")
for name, age, job in cursor.fetchall():
    job = job if job else "Безработный"
    print(f"Имя: {name}, Возраст: {age}, Профессия: {job}")

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
