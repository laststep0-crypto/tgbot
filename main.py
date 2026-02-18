import telebot
import os
from telebot import types
from flask import Flask
import threading

TOKEN = os.getenv('TOKEN')
print("TOKEN в Render начинается так:", str(TOKEN)[:20])
if not TOKEN:
    print("❌ TOKEN не найден!")
    exit()

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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
        except Exception as e:
            bot.send_message(call.message.chat.id, f'❌ Файл не найден: {e}')
    bot.answer_callback_query(call.id)

@app.route('/')
def index():
    return 'Bot is running', 200

def run_bot():
    print("🤖 Запускаю polling...")
    bot.infinity_polling()

if __name__ == '__main__':
    # запуск бота в отдельном потоке
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()

    # Flask-сервер для Render (порт обязателен)
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Flask слушает порт {port}")
    app.run(host='0.0.0.0', port=port)