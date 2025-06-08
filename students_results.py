import sqlite3

conn = sqlite3.connect("students_result.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students_info(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL     
)
''')
cursor.execute("INSERT INTO students_info(name, email) VALUES ('Ksenia', 'ksenia@example.com')")
cursor.execute("INSERT INTO students_info(name, email) VALUES ('Max', 'max@example.com')")
cursor.execute("INSERT INTO students_info(name, email) VALUES ('Anna', 'anna@example.com')")

cursor.execute('''
CREATE TABLE IF NOT EXISTS tests_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    students_id  INTEGER,
    test_name TEXT,
    score INTEGER
)
''')
cursor.execute("INSERT INTO tests_results(students_id, test_name, score) VALUES(1, 'Theory qa', 90)")
cursor.execute("INSERT INTO tests_results(students_id, test_name, score) VALUES(2, 'Theory frontend', 30)")
cursor.execute("INSERT INTO tests_results(students_id, test_name, score) VALUES(3, 'Theory backend', 60)")
cursor.execute("INSERT INTO tests_results(students_id, test_name, score) VALUES(3, 'Theory qa', 20)")
cursor.execute("INSERT INTO tests_results(students_id, test_name, score) VALUES(2, 'Theory frontend', 100)")

conn.commit()

print("\n Имя, email, СРЕДНИЙ балл КАЖДОГО студента(по убыванию):")
cursor.execute('''
SELECT students_info.name, students_info.email, AVG(tests_results.score) AS avg_score
FROM students_info
JOIN tests_results ON students_info.id = tests_results.students_id
GROUP BY students_info.id
ORDER BY avg_score DESC
''')
print(cursor.fetchall())
conn.close()