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

print("\n Повторение БД")
conn1 = sqlite3.connect("test.db")
cursor1 = conn1.cursor()

cursor1.execute("SELECT * FROM users")
users = cursor1.fetchall()
print("Пользователи из test.db:")
for user in users:
    print(user)

conn.close()

conn2 = sqlite3.connect("books.db")
cursor2 = conn2.cursor()

cursor2.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL
)
''')
cursor2.execute("INSERT INTO books (title, author) VALUES ('1984', 'Джордж Оруэлл')")
cursor2.execute("INSERT INTO books (title, author) VALUES ('Мастер и Маргарита', 'Булгаков')")
conn2.commit()

cursor2.execute("SELECT * FROM books")
books = cursor2.fetchall()
print("\n Книги из books.db:")
for book in books:
    print(book)
conn2.close()

print("\n products")
# подключение к БД
conn3 = sqlite3.connect("products.db")
cursor3 = conn3.cursor()
# создаем таблицу
cursor3.execute('''
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER 
)
''')
# добавим товары
cursor3.execute("INSERT INTO products (name, price) VALUES ('Хлеб', 50)")
cursor3.execute("INSERT INTO products (name, price) VALUES ('Молоко', 80)")
cursor3.execute("INSERT INTO products (name, price) VALUES ('Яйца', 90)")
conn3.commit()
# получаем и выводим товары
cursor3.execute("SELECT * FROM products")
products = cursor3.fetchall()
# обновляем цкну одного товара
cursor3.execute("UPDATE products SET price = 100 WHERE name='Яйца'")
conn3.commit()
# удаляем один товар
cursor3.execute("DELETE FROM products WHERE name='Молоко'")
conn3.commit()
# выводим новую версию списка
cursor3.execute("SELECT * FROM products")
products = cursor3.fetchall()
# выводим результат
print("\n Продукты после изменений:")
for product in products:
    print(product)
# закрываем соединение
conn.close()

print("\n clients")
conn4 = sqlite3.connect("clients.db")
cursor4 = conn4.cursor()

cursor4.execute('''
CREATE TABLE IF NOT EXISTS clients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    city TEXT NOT NULL,
    balance INTEGER
)              
''')
cursor4.execute("INSERT INTO clients(full_name, city, balance) VALUES('Ольга Соколова', 'Москва', 1200)")
cursor4.execute("INSERT INTO clients(full_name, city, balance) VALUES('Иван Петров', 'Екатеринбург', 800)")
cursor4.execute("INSERT INTO clients(full_name, city, balance) VALUES('Мария Кузнецова', 'Москва', 600)")
conn4.commit()

cursor4.execute("UPDATE clients SET balance = 950 WHERE full_name = 'Иван Петров'")
conn4.commit()

cursor4.execute("DELETE FROM clients WHERE full_name='Мария Кузнецова'")
conn4.commit()

cursor4.execute("SELECT * FROM clients")
clients = cursor4.fetchall()
print("\n Список клиентов после изменений:")
for client in clients:
    print(client)

print("\n Клиенты из Москвы:")
cursor4.execute("SELECT * FROM clients WHERE city = 'Москва'")
clients = cursor4.fetchall()
for client in clients:
    print(client)

print("\n Клиенты с балансом больше 1000:")
cursor4.execute("SELECT * FROM clients WHERE balance >= 1000")
clients = cursor4.fetchall()
for client in clients:
    print(client)

print("\n Сортировка по имени в алфавитном порядке")
cursor4.execute("SELECT * FROM clients ORDER BY full_name ASC")
clients = cursor4.fetchall()
print(clients)

print("\n Сортировка клиентов по убыванию баланса:")
cursor4.execute("SELECT * FROM clients ORDER BY balance DESC")
print(cursor4.fetchall())

print("\n Имена и баланс клиентов")
cursor4.execute("SELECT full_name, balance FROM clients")
print(cursor4.fetchall())

conn4.close()

conn5 = sqlite3.connect("clients.db")
cursor5 = conn5.cursor()
print("\n Клиенты, живущие в Екатеринбурге:")
cursor5.execute("SELECT * FROM clients WHERE city='Екатеринбург'")
clients = cursor5.fetchall()
for client in clients:
    print(client)

print("\n Имена и балан клиентов, баланс, которых меньше 1000:")
cursor5.execute("SELECT full_name, balance FROM clients WHERE balance < 1000")
print(cursor5.fetchall())

print("\n Отсортированные города клиентов  в алфавитном порядке:")
cursor5.execute("SELECT * FROM clients ORDER BY city ASC")
print(cursor5.fetchall())

print("\n Имена клиентов из Москвы, отсортированы по убыванию баланса:")
cursor5.execute("SELECT full_name FROM clients WHERE city='Москва' ORDER BY balance DESC")
print(cursor5.fetchall())
conn5.close()


print("\n QA_engineers")
conn6 = sqlite3.connect("company.db")
cursor6 = conn6.cursor()
# Таблица QA - engineers
cursor6.execute('''
CREATE TABLE IF NOT EXISTS qa_engineers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    city TEXT NOT NULL
)             
''')
cursor6.execute("INSERT INTO qa_engineers(name, email, age, city) VALUES('Ксения', 'kseniatest@mail.ru', 25, 'Москва')")
cursor6.execute("INSERT INTO qa_engineers(name, email, age, city) VALUES('Анна', 'annatest@mail.ru', 30, 'Пермь')")
cursor6.execute("INSERT INTO qa_engineers(name, email, age, city) VALUES('Олег', 'olegtest@mail.ru', 28, 'Казань')")
cursor6.execute("INSERT INTO qa_engineers(name, email, age, city) VALUES('Иван', 'ivantest@mail.ru', 23, 'Москва')")
conn6.commit()

# Таблица orders
cursor6.execute('''
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    status TEXT NOT NULL
)
''')
cursor6.execute("INSERT INTO orders(user_id, amount, status) VALUES(1, 1500, 'completed')")
cursor6.execute("INSERT INTO orders(user_id, amount, status) VALUES(2, 3000, 'canceled')")
cursor6.execute("INSERT INTO orders(user_id, amount, status) VALUES(3, 500, 'completed')")
cursor6.execute("INSERT INTO orders(user_id, amount, status) VALUES(1, 2000, 'completed')")
conn6.commit()


print("\n Пользователи старше 25 лет")
cursor6.execute("SELECT * FROM qa_engineers WHERE age > 25")
print(cursor6.fetchall())

print("\n Имена и email только из Москвы")
cursor6.execute("SELECT name, email FROM qa_engineers WHERE city='Москва'")
print(cursor6.fetchall())

print("\n Пользователи с заказами со статусом 'completed'")
cursor6.execute('''
SELECT qa_engineers.name, qa_engineers.city 
FROM qa_engineers 
JOIN orders ON qa_engineers.id = orders.user_id 
WHERE orders.status = 'completed'
''')
print(cursor6.fetchall())
conn6.close()

print("\n Seller_sales")
conn7 = sqlite3.connect("seller_sale.db")
cursor7 = conn7.cursor()
# Seller
cursor7.execute('''
CREATE TABLE IF NOT  EXISTS seller(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL
)
''')

cursor7.execute("INSERT INTO seller(name, city) VALUES('Ksenia', 'Moscow')")
cursor7.execute("INSERT INTO seller(name, city) VALUES('Anna', 'Perm')")
cursor7.execute("INSERT INTO seller(name, city) VALUES('Ivan', 'Kazan')")
conn7.commit()
# Sales
cursor7.execute('''
CREATE TABLE IF NOT EXISTS sale(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product TEXT NOT NULL,
    amount INTEGER,
    status TEXT NOT NULL           
)
''')
cursor7.execute("INSERT INTO sale(user_id, product, amount, status) VALUES(1, 'Laptop', 1200, 'completed')")
cursor7.execute("INSERT INTO sale(user_id, product, amount, status) VALUES(1, 'Headphones', 200, 'completed')")
cursor7.execute("INSERT INTO sale(user_id, product, amount, status) VALUES(2, 'Smartphone', 800, 'canceled')")
cursor7.execute("INSERT INTO sale(user_id, product, amount, status) VALUES(3, 'Keyboard', 100, 'completed')")
conn7.commit()

print("\n Имя пользователя, название товара и сумма только 'completed'")
cursor7.execute('''
SELECT seller.name, sale.product, sale.amount
FROM seller
JOIN sale ON seller.id = sale.user_id
WHERE sale.status = 'completed'
''')
print(cursor7.fetchall())

print("\n Имя пользователя, город, общая сумма заказов, только'completed'")
cursor7.execute('''
SELECT seller.name, seller.city, SUM(sale.amount) AS total_sales
FROM seller
JOIN sale ON seller.id = sale.user_id
WHERE sale.status = 'completed'
GROUP BY seller.id, seller.name, seller.city
''')
print(cursor7.fetchall())
conn7.close()

