import sqlite3

conn = sqlite3.connect("practice.db")
cursor = conn.cursor()

# users_email
cursor.execute('''
CREATE TABLE IF NOT EXISTS users_email(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
''')
cursor.execute("INSERT INTO users_email(name, email) VALUES('Anna', 'anya@example.com')")
cursor.execute("INSERT INTO users_email(name, email) VALUES('Boris', 'boris@example.com')")
cursor.execute("INSERT INTO users_email(name, email) VALUES('Ksenia', 'ksenia@example.com')")

#orders_amount
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders_amount(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER
)
''')
cursor.execute("INSERT INTO orders_amount(user_id, amount) VALUES(1, 1500)")
cursor.execute("INSERT INTO orders_amount(user_id, amount) VALUES(2, 2300)")
cursor.execute("INSERT INTO orders_amount(user_id, amount) VALUES(1, 500)")
cursor.execute("INSERT INTO orders_amount(user_id, amount) VALUES(3, 1200)")
conn.commit()

print("\n Все заказы  с именем пользователя и email")
cursor.execute('''
    SELECT orders_amount.id, users_email.name, users_email.email
    FROM orders_amount
    JOIN users_email ON orders_amount.user_id = users_email.id
''')
print(cursor.fetchall())

print("\n Сумма всех заказов для каждого пользователя:")
cursor.execute('''
SELECT users_email.name, SUM(orders_amount.amount) AS total_amount
FROM orders_amount
JOIN users_email ON orders_amount.user_id = users_email.id
GROUP BY users_email.name
''')
print(cursor.fetchall())

print("\n Пользователи, у которых сумма заказа больше 1000:")
cursor.execute('''
SELECT users_email.name, orders_amount.amount
FROM users_email
JOIN orders_amount ON users_email.id = orders_amount.user_id
WHERE orders_amount.amount > 1000
''')
print(cursor.fetchall())

print("\n Пользователи, у которых сумма всех заказов больше 2000:")
cursor.execute('''
SELECT users_email.name,users_email.email, orders_amount.amount AS total
FROM users_email
JOIN orders_amount ON users_email.id = orders_amount.user_id
GROUP BY users_email.id
HAVING SUM(orders_amount.amount) > 2000
''')
print(cursor.fetchall())

print("\n Пользователи, которые не сделали ни одного заказа:")
cursor.execute('''
SELECT users_email.name, users_email.email
FROM users_email
LEFT JOIN orders_amount ON users_email.id = orders_amount.user_id
WHERE users_email.id IS NULL
''')
print(cursor.fetchall())

print("\n Заказы на сумму больше 1000(ID, name, email, amount)")
cursor.execute('''
SELECT orders_amount.id, users_email.name, users_email.email, orders_amount.amount
FROM users_email
JOIN orders_amount ON users_email.id = orders_amount.user_id
WHERE orders_amount.amount > 1000
''')
print(cursor.fetchall())
conn.close()