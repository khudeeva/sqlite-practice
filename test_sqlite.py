import sqlite3
import unittest

class TestSQLiteDatabase(unittest.TestCase):
    def setUp(self):
        """Создаём тестовую БД перед каждым тестом"""
        self.conn = sqlite3.connect(":memory:")  # Используем временную БД (не сохраняется на диск)
        self.cursor = self.conn.cursor()

        # Создаём таблицу
        self.cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        ''')

    def tearDown(self):
        """Закрываем соединение после каждого теста"""
        self.conn.close()

    def test_insert_user(self):
        """Проверяем, что можно вставить пользователя"""
        self.cursor.execute("INSERT INTO users (name, age) VALUES ('Анна', 22)")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()

        self.assertEqual(len(users), 1)  # Должен быть 1 пользователь
        self.assertEqual(users[0][1], "Анна")  # Имя должно быть "Анна"
        self.assertEqual(users[0][2], 22)  # Возраст должен быть 22

    def test_update_user(self):
        """Проверяем, что можно обновить возраст пользователя"""
        self.cursor.execute("INSERT INTO users (name, age) VALUES ('Иван', 29)")
        self.conn.commit()

        self.cursor.execute("UPDATE users SET age = 30 WHERE name = 'Иван'")
        self.conn.commit()

        self.cursor.execute("SELECT age FROM users WHERE name = 'Иван'")
        updated_age = self.cursor.fetchone()[0]

        self.assertEqual(updated_age, 30)  # Должно быть 30

    def test_delete_user(self):
        """Проверяем, что можно удалить пользователя"""
        self.cursor.execute("INSERT INTO users (name, age) VALUES ('Мария', 34)")
        self.conn.commit()

        self.cursor.execute("DELETE FROM users WHERE name = 'Мария'")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM users WHERE name = 'Мария'")
        user = self.cursor.fetchone()

        self.assertIsNone(user)  # Должно быть None, так как запись удалена

    def test_select_users(self):
        """Проверяем выборку пользователей"""
        self.cursor.execute("INSERT INTO users (name, age) VALUES ('Анна', 22)")
        self.cursor.execute("INSERT INTO users (name, age) VALUES ('Иван', 29)")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM users WHERE age > 25")
        users = self.cursor.fetchall()

        self.assertEqual(len(users), 1)  # Должен быть 1 пользователь (Иван)
        self.assertEqual(users[0][1], "Иван")  # Имя должно быть "Иван"

if __name__ == "__main__":
    unittest.main()
