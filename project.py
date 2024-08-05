import telebot
from telebot import types
import os
import subprocess
import pyautogui
import threading

bot = telebot.TeleBot('7429781312:AAFzIFy7dvJLQtGbXaAfXZwms9TFjXNmpbs')


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Запустить Chrome', callback_data='Chrome')
    btn2 = types.InlineKeyboardButton(text='Сделать скриншот', callback_data='Screenshot')
    btn3 = types.InlineKeyboardButton(text='Запустить код', callback_data='Python')
    kb.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     'Привет! Я бот для дистанционного управления компьютером! Выбери действие при помощи кнопок ниже!',
                     reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    print(query.data)
    if query.data == 'Chrome':
        threading.Thread(target=chrome, args=(query,)).start()
    elif query.data == 'Screenshot':
        threading.Thread(target=screenshot, args=(query,)).start()
    elif query.data == 'Python':
        bot.edit_message_text(message_id=query.message.id, chat_id=query.from_user.id,
                              text="Отправьте текст для запуска",
                              reply_markup=types.InlineKeyboardMarkup().add(
                                  types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))
        bot.register_next_step_handler(query.message, code)
    elif query.data == 'Menu':
        menu(query.message)


def screenshot(query):
    bot.delete_message(query.message.chat.id, query.message.message_id)
    bot.send_photo(chat_id=query.message.chat.id, photo=pyautogui.screenshot(),
                   reply_markup=types.InlineKeyboardMarkup().add(
                       types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def chrome(query):
    os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    bot.edit_message_text(message_id=query.message.id, chat_id=query.message.chat.id,
                          text="Запустил приложение " + query.data,
                          reply_markup=types.InlineKeyboardMarkup().add(
                              types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def code(message):
    with open('tets.py', 'w', encoding='UTF-8') as f:
        f.write(message.text)
    try:
        result = subprocess.run(['python', 'tets.py'], capture_output=True, text=True, check=True, encoding='utf-8')
        if result.stdout != "":
            bot.send_message(message.chat.id, result.stdout,
                             reply_markup=types.InlineKeyboardMarkup().add(
                                 types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))
    except subprocess.CalledProcessError as e:
        bot.send_message(message.chat.id, e.stderr,
                         reply_markup=types.InlineKeyboardMarkup().add(
                             types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def menu(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Запустить Chrome', callback_data='Chrome')
    btn2 = types.InlineKeyboardButton(text='Сделать скриншот', callback_data='Screenshot')
    btn3 = types.InlineKeyboardButton(text='Запустить код', callback_data='Python')
    kb.add(btn1, btn2, btn3)
    if message.content_type!='text':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(chat_id=message.chat.id,
                         text='Главное меню',
                         reply_markup=kb)
    else:
        bot.edit_message_text(message_id=message.id, chat_id=message.chat.id, text='Главное меню', reply_markup=kb)


if __name__ == '__main__':
    bot.infinity_polling()
