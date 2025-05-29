import sqlite3

# Подключение к БД
conn = sqlite3.connect("airplane_pilot_flight.db")
cursor = conn.cursor()

# Удаляем таблицы, если они уже есть (чтобы не было ошибок и дубликатов)
cursor.execute("DROP TABLE IF EXISTS airplane_pilot")
cursor.execute("DROP TABLE IF EXISTS airplane")
cursor.execute("DROP TABLE IF EXISTS pilot")

# Создание таблицы пилотов
cursor.execute('''
CREATE TABLE pilot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
)
''')

# Добавляем пилотов
cursor.execute("INSERT INTO pilot(first_name, last_name) VALUES('Ivan', 'Petrov')")
cursor.execute("INSERT INTO pilot(first_name, last_name) VALUES('Anna', 'Sidorova')")
cursor.execute("INSERT INTO pilot(first_name, last_name) VALUES('John', 'Smith')")

# Создание таблицы самолётов
cursor.execute('''
CREATE TABLE airplane (
    airplane_id INTEGER PRIMARY KEY,
    model TEXT NOT NULL
)
''')

# Добавляем самолёты
cursor.execute("INSERT INTO airplane(airplane_id, model) VALUES(1, 'Сухой')")
cursor.execute("INSERT INTO airplane(airplane_id, model) VALUES(2, 'Boeing')")
cursor.execute("INSERT INTO airplane(airplane_id, model) VALUES(3, 'Сухой')")

# Создание таблицы полётов
cursor.execute('''
CREATE TABLE airplane_pilot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pilot_id INTEGER,
    airplane_id INTEGER,
    flight_date TEXT
)
''')

# Добавляем полёты
cursor.execute("INSERT INTO airplane_pilot(pilot_id, airplane_id, flight_date) VALUES(1, 1, '2022-02-15')")  # Petrov, Сухой
cursor.execute("INSERT INTO airplane_pilot(pilot_id, airplane_id, flight_date) VALUES(1, 2, '2022-02-07')")  # Petrov, Boeing
cursor.execute("INSERT INTO airplane_pilot(pilot_id, airplane_id, flight_date) VALUES(2, 3, '2022-02-10')")  # Sidorova, Сухой
cursor.execute("INSERT INTO airplane_pilot(pilot_id, airplane_id, flight_date) VALUES(3, 1, '2022-02-25')")  # Smith, Сухой
cursor.execute("INSERT INTO airplane_pilot(pilot_id, airplane_id, flight_date) VALUES(3, 3, '2022-03-01')")  # Smith, Сухой — вне периода

conn.commit()

# Выполняем SQL-запрос
cursor.execute('''
SELECT 
    p.last_name,
    COUNT(*) AS flight_count
FROM 
    airplane_pilot ap
JOIN 
    pilot p ON ap.pilot_id = p.id
JOIN 
    airplane a ON ap.airplane_id = a.airplane_id
WHERE 
    a.model = 'Сухой'
    AND ap.flight_date BETWEEN '2022-02-01' AND '2022-02-28'
GROUP BY 
    p.last_name;
''')

# Вывод результата
print(cursor.fetchall())

# Закрытие соединения
conn.close()
