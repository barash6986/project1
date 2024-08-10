import os
import subprocess
import threading

import pyautogui
import telebot
import win10toast
from googlesearch import search
from telebot import types

bot = telebot.TeleBot('7429781312:AAFzIFy7dvJLQtGbXaAfXZwms9TFjXNmpbs')


@bot.message_handler(commands=['start'])
def start(message):
    kb = main_menu()
    bot.send_message(message.chat.id,
                     'Привет! Я бот для дистанционного управления компьютером! Выбери действие при помощи кнопок ниже!',
                     reply_markup=kb)

@bot.message_handler(commands=['off'])
def off(message):
    bot.send_message(chat_id=message.from_user.id, text='Выключаю компьютер')
    os.system('shutdown /s /t 1')


@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    print(query.data)
    if query.data == 'Chrome':
        threading.Thread(target=chrome, args=(query,)).start()
    elif query.data == 'Pycharm':
        threading.Thread(target=pycharm, args=(query,)).start()
    elif query.data == 'Edge':
        threading.Thread(target=edge, args=(query,)).start()
    elif query.data == 'Screenshot':
        threading.Thread(target=screenshot, args=(query,)).start()
    elif query.data == 'Python':
        bot.edit_message_text(message_id=query.message.id, chat_id=query.from_user.id,
                              text="Отправьте текст для запуска (только python код)",
                              reply_markup=types.InlineKeyboardMarkup().add(
                                  types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))
        bot.register_next_step_handler(query.message, code)
    elif query.data == 'Menu':
        menu(query.message)
    elif query.data == 'Apps':
        threading.Thread(target=apps, args=(query,)).start()
    elif query.data == 'Search':
        bot.edit_message_text(message_id=query.message.id, chat_id=query.from_user.id,
                              text="Отправьте текст для поиска",
                              reply_markup=types.InlineKeyboardMarkup().add(
                                  types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))
        bot.register_next_step_handler(query.message, search_)
    elif query.data == 'Paint':
        threading.Thread(target=paint, args=(query,)).start()
    elif query.data == 'Off_PC':
        bot.answer_callback_query(query.id, 'Сейчас нельзя это сделать')
    elif query.data == 'Notification':
        bot.edit_message_text(message_id=query.message.id, chat_id=query.from_user.id,
                              text='Введите уведомление для отправки',
                              reply_markup=types.InlineKeyboardMarkup().add(
                                  types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))
        bot.register_next_step_handler(query.message, notification)


def apps(query):
    kb = types.InlineKeyboardMarkup(row_width=4)
    btn1 = types.InlineKeyboardButton(text='Chrome', callback_data='Chrome')
    btn2 = types.InlineKeyboardButton(text='Pycharm', callback_data='Pycharm')
    btn3 = types.InlineKeyboardButton(text='Edge', callback_data='Edge')
    btn5 = types.InlineKeyboardButton(text='Paint', callback_data='Paint')
    btn4 = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')
    kb.add(btn1, btn2, btn3, btn5, btn4)
    bot.edit_message_text(message_id=query.message.id, chat_id=query.from_user.id, text='Выберите приложение которое '
                                                                                        'вы хотите открыть',
                          reply_markup=kb)


def notification(message):
    try:
        toaster = win10toast.ToastNotifier()
        toaster.show_toast(message.text, message.text)
    except:
        pass
    bot.send_message(chat_id=message.chat.id, text='Уведомление успешно отправленно',
                     reply_markup=types.InlineKeyboardMarkup().add(
                         types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def search_(message):
    global url_site
    url_site = ''
    for url in search(message.text, stop=1):
        url_site = url
    if url_site == '':
        bot.send_message(message.chat.id, text='Запрос не найден',
                         reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                             types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))
    else:
        bot.send_message(message.chat.id, text='Перейти на сайт', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text='Переход на сайт', url=url_site),
            types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def paint(query):
    os.startfile('C:\\Windows\\system32\\mspaint.exe')
    bot.edit_message_text(message_id=query.message.id, chat_id=query.message.chat.id,
                          text="Запустил приложение " + query.data,
                          reply_markup=types.InlineKeyboardMarkup().add(
                              types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def screenshot(query):
    bot.send_photo(chat_id=query.message.chat.id, photo=pyautogui.screenshot(),
                   reply_markup=types.InlineKeyboardMarkup().add(
                       types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def chrome(query):
    os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    bot.edit_message_text(message_id=query.message.id, chat_id=query.message.chat.id,
                          text="Запустил приложение " + query.data,
                          reply_markup=types.InlineKeyboardMarkup().add(
                              types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def pycharm(query):
    os.startfile('C:\\Program Files\\JetBrains\\PyCharm 2024.1.4\\bin\\pycharm64.exe')
    bot.edit_message_text(message_id=query.message.id, chat_id=query.message.chat.id,
                          text="Запустил приложение " + query.data,
                          reply_markup=types.InlineKeyboardMarkup().add(
                              types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Menu')))


def edge(query):
    os.startfile('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
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
    kb = main_menu()
    if message.content_type != 'text':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(chat_id=message.chat.id,
                         text='Главное меню',
                         reply_markup=kb)
    else:
        bot.edit_message_text(message_id=message.id, chat_id=message.chat.id, text='Главное меню', reply_markup=kb)


def main_menu():
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Приложения', callback_data='Apps')
    btn2 = types.InlineKeyboardButton(text='Сделать скриншот', callback_data='Screenshot')
    btn3 = types.InlineKeyboardButton(text='Запустить код', callback_data='Python')
    btn4 = types.InlineKeyboardButton(text='Найти информацию', callback_data='Search')
    btn6 = types.InlineKeyboardButton(text='Вывести уведомление на экран', callback_data='Notification')
    btn5 = types.InlineKeyboardButton(text='Выключить компьютер', callback_data='Off_PC')
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return kb


if __name__ == '__main__':
    bot.infinity_polling()
