import telebot
from telebot import types
import os
import subprocess
import pyautogui

bot = telebot.TeleBot('7429781312:AAFzIFy7dvJLQtGbXaAfXZwms9TFjXNmpbs')


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Запустить Chrome', callback_data='Chrome')
    btn2 = types.InlineKeyboardButton(text='Сделать скриншот', callback_data='Screenshot')
    btn3 = types.InlineKeyboardButton(text='Запустить код', callback_data='Python')
    kb.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     'Привет! Я бот для дистанционного управления компьютером! Выбери действие при помощи кнопок ниже!', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    print(query.data)
    if query.data == 'Chrome':
        os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        bot.send_message(query.message.chat.id, "Запустил приложение "+query.data)
        menu(query.message)
    elif query.data == 'Screenshot':
        bot.send_photo(query.message.chat.id, pyautogui.screenshot())
        menu(query.message)
    elif query.data == 'Python':
        bot.send_message(query.from_user.id, "Отправьте текст для запуска")
        bot.register_next_step_handler(query.message, code)


def code(message):
    with open('tets.py', 'w', encoding='UTF-8') as f:
        f.write(message.text)
    try:
        result = subprocess.run(['python', 'tets.py'], capture_output=True, text=True, check=True, encoding='utf-8')
        if result.stdout != "":
            bot.send_message(message.chat.id, result.stdout)
    except subprocess.CalledProcessError as e:
        bot.send_message(message.chat.id, e.stderr)
    menu(message)


def menu(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Запустить Chrome', callback_data='Chrome')
    btn2 = types.InlineKeyboardButton(text='Сделать скриншот', callback_data='Screenshot')
    btn3 = types.InlineKeyboardButton(text='Запустить код', callback_data='Python')
    kb.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     'Главное меню',
                     reply_markup=kb)


if __name__ == '__main__':
    bot.infinity_polling()
