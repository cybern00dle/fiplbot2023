import pandas as pd
import telebot

from bot_functions import read_user_info, show_timetable
from fipl_data import formulas, materials, minors, students, timetable

bot = telebot.TeleBot('6687870375:AAETInBz2DPYABkopwZbvZF0WEPLfxwHzg8')

user_info = {}
user_id = ''
days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']


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
        minor_row = minors[minors['ФИО'].str.lower() == user_info['name']]
        link = minor_row['Ссылка на майнор'].squeeze()
        bot.send_message(message.chat.id, f'Вот твоя ссылка:\n{link}')
    elif response == 'формулы оценки':
        form_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        form_markup.row('Теория языка', 'НИС "Тестирование и экспертиза в лингвистических исследованиях"')
        form_markup.row('Технологии разработки баз данных', 'Практикум по разработке лингвистических систем')
        form_markup.row('НИС "Анализ и синтез звучащей речи"', 'Психолингвистика')
        msg = bot.send_message(message.chat.id, 'Какой предмет тебе нужен?', reply_markup=form_markup)
        bot.register_next_step_handler(msg, handle_formulas)
    elif response == 'дедлайны':
        pass
    elif response == 'оценить бота':
        pass
    else:
        bot.send_message(message.chat.id, 'Я не понимаю твой запрос, попробуй ещё раз.')


def handle_timetable(message):
    if message.text.lower().strip() == 'день':
        msg = bot.send_message(message.chat.id, 'Какой день недели тебе нужен?')
        bot.register_next_step_handler(msg, handle_time_day)
    elif message.text.lower().strip() == 'неделя':
        resp = ''
        for day in days:
            resp += show_timetable(timetable, user_info, day)
        bot.send_message(message.chat.id, resp)
    else:
        bot.send_message(message.chat.id, 'Я не могу показать расписание. Период введён неправильно.')


def handle_time_day(message):
    day = message.text.lower().strip()
    if day in days:
        resp = show_timetable(timetable, user_info, day)
        bot.send_message(message.chat.id, resp)
    else:
        bot.send_message(message.chat.id, 'Я не могу показать расписание на этот день.')


def handle_materials(message):
    if materials['Дисциплина'].str.lower().isin([message.text.lower().strip()]).any():
        mats = materials[materials['Дисциплина'].str.lower() == message.text.lower().strip()][
            'Ссылка на материалы'].squeeze()
        bot.send_message(message.chat.id, f'Вот ссылка:\n{mats}')
    else:
        bot.send_message(message.chat.id, 'Таких материалов у меня нет.')


def handle_formulas(message):
    if formulas['Дисциплины'].str.lower().isin([message.text.lower().strip()]).any():
        form = formulas[formulas['Дисциплины'].str.lower() == message.text.lower().strip()][
            'Формулы оценивания'].squeeze()
        bot.send_message(message.chat.id, f'Вот формула:\n{form}')
    else:
        bot.send_message(message.chat.id, 'Такой формулы у меня нет.')


bot.polling(none_stop=True)
