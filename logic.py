import sqlite3
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

# Подключение к базе данных
conn = sqlite3.connect('bot.db')
cursor = conn.cursor()

# Создаем таблицы, если их нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    chat_id INTEGER,
    last_interaction TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY,
    category TEXT,
    title TEXT,
    link TEXT,
    description TEXT
)
''')
conn.commit()

# Функция для регистрации нового пользователя
def register_user(chat_id, username):
    cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (username, chat_id, last_interaction) VALUES (?, ?, ?)',
                       (username, chat_id, None))
        conn.commit()

# Функция для добавления рекомендации
def add_recommendation(category, title, link, description):
    cursor.execute('INSERT INTO recommendations (category, title, link, description) VALUES (?, ?, ?, ?)',
                   (category, title, link, description))
    conn.commit()

# Функция для получения рекомендаций по категории
def get_recommendations(category):
    cursor.execute('SELECT title, link, description FROM recommendations WHERE category = ?', (category,))
    return cursor.fetchall()

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    register_user(chat_id, username)
    
    update.message.reply_text(
        "*Привет!*\n"
        "Я бот, который поможет тебе с полезной документацией и гайдами. "
        "Для начала выбери категорию или спроси меня о чем-то конкретном.",
        parse_mode=ParseMode.MARKDOWN
    )

# Команда для получения рекомендаций
def recommend(update: Update, context: CallbackContext) -> None:
    if context.args:
        category = context.args[0].lower()
        recommendations = get_recommendations(category)
        if recommendations:
            response = f"Вот что я нашел по категории *{category}*:\n\n"
            for title, link, description in recommendations:
                response += f"*{title}*\n[{link}]({link})\n_{description}_\n\n"
            update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(f"К сожалению, я не нашел ничего по категории *{category}*.", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Пожалуйста, укажи категорию после команды /recommend.", parse_mode=ParseMode.MARKDOWN)

# Основная функция для запуска бота
def main():
    updater = Updater("YOUR_BOT_API_KEY")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("recommend", recommend))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

