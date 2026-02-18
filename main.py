import telebot
import os
from telebot import types

TOKEN = os.getenv('TOKEN')
print("TOKEN в Render начинается так:", str(TOKEN)[:20])
if not TOKEN:
    print("❌ TOKEN не найден!")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('📄 Получить документ', callback_data='doc')
    markup.add(btn)
    bot.send_message(message.chat.id, '👋 Привет! Нажми за файлом:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'doc':
        try:
            with open('document.docx', 'rb') as f:
                bot.send_document(call.message.chat.id, f, caption='📄 Вот твой .docx!')
        except:
            bot.send_message(call.message.chat.id, '❌ Файл не найден')
    bot.answer_callback_query(call.id)

print("🤖 Бот запущен!")
bot.infinity_polling()