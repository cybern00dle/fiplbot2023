import pandas as pd
import telebot

from bot_functions import read_user_info, show_timetable
from fipl_data import formulas, materials, minors, students, timetable

bot = telebot.TeleBot('6687870375:AAETInBz2DPYABkopwZbvZF0WEPLfxwHzg8')

user_info = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, '''Привет! Это ФиПЛ-бот.
Для начала работы введи свои ФИО, пожалуйста.''')
    bot.register_next_step_handler(msg, handle_name)


def handle_name(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Расписание', 'Учебные материалы')
    user_markup.row('Майноры', 'Формулы оценки')
    user_markup.row('Дедлайны', 'Оценить бота')
    fio = message.text.lower().strip()
    if students['ФИО'].str.lower().isin([fio]).any():
        user_info['name'] = fio
        read_user_info(students, user_info)
        msg = bot.send_message(message.chat.id, 'Спасибо! Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        bot.send_message(message.chat.id, 'Такие ФИО я не знаю!')


@bot.message_handler(content_types=['text'])
def handle_options(message):
    response = message.text.lower().strip()
    if response == 'расписание':
        time_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        time_markup.row('День', 'Неделя')
        msg = bot.send_message(message.chat.id, 'На какой период тебе нужно расписание?', reply_markup=time_markup)
        bot.register_next_step_handler(msg, handle_timetable)
    elif response == 'учебные материалы':
        mat_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        mat_markup.row('Теория языка 2 курс', 'Теория языка 3 курс')
        mat_markup.row('Немецкий язык', 'Французский язык')
        mat_markup.row('Функциональная стилистика', 'НИС "Анализ и синтез звучащей речи"')
        mat_markup.row('Технологии разработки баз данных')
        msg = bot.send_message(message.chat.id, 'Какой предмет тебе нужен?', reply_markup=mat_markup)
        bot.register_next_step_handler(msg, handle_materials)
    elif response == 'майноры':
        bot.register_next_step_handler(message, handle_minors)
    elif response == 'формулы оценки':
        pass
    elif response == 'дедлайны':
        pass
    elif response == 'оценить бота':
        pass
    else:
        bot.send_message(message.chat.id, 'Я не понимаю твой запрос, попробуй ещё раз.')


def handle_timetable(message):
    if message.text == 'День':
        msg = bot.send_message(message.chat.id, 'Какой день недели тебе нужен?')
        bot.register_next_step_handler(msg, handle_time_day)
    else:
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
        resp = ''
        for day in days:
            day_resp = show_timetable(timetable, user_info, day)
            resp += day_resp
        bot.send_message(message.chat.id, resp)


def handle_time_day(message):
    day = message.text.lower().strip()
    resp = show_timetable(timetable, user_info, day)
    bot.send_message(message.chat.id, resp)


def handle_materials(message):
    mats = materials[materials['Дисциплина'] == message.text]['Ссылка на материалы'].squeeze()
    bot.send_message(message.chat.id, f'Вот ссылка:\n{mats}')


def handle_minors(message):
    minor_row = minors[minors['ФИО'].str.lower() == user_info['name']]
    link = minor_row['Ссылка на майнор'].squeeze()
    bot.send_message(message.chat.id, f'Вот твоя ссылка:\n{link}')


def handle_formulas(message):



bot.polling(none_stop=True)
