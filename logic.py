import sqlite3
from config import DATABASE
from datetime import datetime

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Создаем таблицу для учета финансов
cursor.execute('''
CREATE TABLE IF NOT EXISTS finance (
    id INTEGER PRIMARY KEY,
    date TEXT,
    description TEXT,
    amount REAL
)
''')
conn.commit()

# Функция для добавления дохода/расхода
def add_transaction(description, amount):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    INSERT INTO finance (date, description, amount)
    VALUES (?, ?, ?)
    ''', (date, description, amount))
    conn.commit()
    print(f'Транзакция добавлена: {description} | Сумма: {amount}')

# Функция для получения баланса
def get_balance():
    cursor.execute('SELECT SUM(amount) FROM finance')
    balance = cursor.fetchone()[0]
    return balance if balance else 0

# Функция для получения всех транзакций
def get_transactions():
    cursor.execute('SELECT * FROM finance')
    return cursor.fetchall()

print(f'Текущий баланс: {get_balance()}')
print('Все транзакции:')
for transaction in get_transactions():
    print(transaction)


conn.close()
