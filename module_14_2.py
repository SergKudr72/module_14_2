import sqlite3
connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

# создание таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
) 
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

cursor.execute('DELETE FROM Users')  # Очистка таблицы перед её заполнением

# заполнение таблицы 10-ю записями
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", f"{i*10}", "1000"))

for i in range(1, 11, 2): # обновление баланса на 500 для каждой 2-ой записи, начиная с 1-ой
    cursor.execute("UPDATE Users SET balance = ? WHERE id = ?", (500, i))

for i in range(1, 11, 3): # удаление каждой 3-ой записи, начиная с 1-ой
    cursor.execute("DELETE FROM Users WHERE id = ?", (i,))

# выборка всех записей, где возраст не равен 60 (без id)
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
for user in users:
    username, email, age, balance = user
    # print(f'Имя: {username} | ', f'Почта: {email} | ', f'Возраст: {age} | ', f'Баланс: {balance}')

# удаление id = 6
cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

# считаем общее кол-во записей
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]
# print(total_users)

# считаем суммы всех балансов
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]
# print(all_balances)

# выводим в консоль средний баланс всех пользователей
print(all_balances / total_users)

connection.commit()
connection.close()
