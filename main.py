import telebot
from config import TOKEN

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """
Привет, это бот, который будет считать твои расходы и доходы. Следи за своими расходами!
""")


@bot.message_handler()
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()