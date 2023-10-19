import atexit
import pandas as pd
import telebot

from bot_functions import authorize_user, get_deadlines, read_user_info, register_user, show_timetable
from fipl_data import faq, formulas, materials, minors, users, reviews, students, timetable

bot = telebot.TeleBot('6687870375:AAETInBz2DPYABkopwZbvZF0WEPLfxwHzg8')

user_info = {}
user_id = ''
days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
review = {}

user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup.row('Расписание', 'Учебные материалы')
user_markup.row('Майноры', 'Формулы оценки')
user_markup.row('Дедлайны', 'Оценить бота')
user_markup.row('Решение проблем и поддержка')


@bot.message_handler(commands=['start', 'reset'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, '''Привет! Это ФиПЛ-бот.
Для начала работы введи свои ФИО, пожалуйста.''')
    bot.register_next_step_handler(msg, handle_name)


def handle_name(message):
    fio = message.text.lower().strip()
    if students['ФИО'].str.lower().isin([fio]).any():
        user_info['name'] = fio
        user_info['user_id'] = message.chat.id
        register_user(users, message.chat.id, user_info['name'])
        read_user_info(students, user_info)
        msg = bot.send_message(message.chat.id, 'Спасибо! Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Такие ФИО я не знаю! Попробуй ещё раз.')
        bot.register_next_step_handler(msg, handle_name)


@bot.message_handler(content_types=['text'])
def handle_options(message):
    if not user_info:
        user_info['user_id'] = message.chat.id
        user_info['name'] = authorize_user(users, message.chat.id)
        read_user_info(students, user_info)

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
        link = minors[minors['ФИО'].str.lower() == user_info['name']]['Ссылка на майнор'].squeeze()
        bot.send_message(message.chat.id, f'Вот твоя ссылка:\n{link}')

    elif response == 'формулы оценки':
        form_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        form_markup.row('Теория языка', 'НИС "Тестирование и экспертиза в лингвистических исследованиях"')
        form_markup.row('Технологии разработки баз данных', 'Практикум по разработке лингвистических систем')
        form_markup.row('НИС "Анализ и синтез звучащей речи"', 'Психолингвистика')
        msg = bot.send_message(message.chat.id, 'Какой предмет тебе нужен?', reply_markup=form_markup)
        bot.register_next_step_handler(msg, handle_formulas)

    elif response == 'дедлайны':
        dd_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        dd_markup.row('Ближайший день')
        dd_markup.row('Ближайшая неделя')
        msg = bot.send_message(message.chat.id, 'На какой период тебе нужны дедлайны?', reply_markup=dd_markup)
        bot.register_next_step_handler(msg, handle_deadlines)

    elif response == 'оценить бота':
        ev_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        ev_markup.row('1', '2', '3', '4', '5')
        msg = bot.send_message(message.chat.id, 'Оцени работу бота по шкале от 1 до 5, пожалуйста.',
                               reply_markup=ev_markup)
        bot.register_next_step_handler(msg, handle_mark)

    elif response == 'решение проблем и поддержка':
        msg = bot.send_message(message.chat.id, faq)
        bot.register_next_step_handler(msg, handle_options)

    elif response == '/start' or response == '/reset':
        msg = bot.send_message(message.chat.id, 'Введи ФИО, пожалуйста.')
        bot.register_next_step_handler(msg, handle_name)

    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)

    else:
        msg = bot.send_message(message.chat.id, 'Я не понимаю твой запрос, попробуй ещё раз.')
        bot.register_next_step_handler(msg, handle_options)


def handle_timetable(message):
    if message.text.lower().strip() == 'день':
        week_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        week_markup.row('Понедельник', 'Вторник')
        week_markup.row('Среда', 'Четверг')
        week_markup.row('Пятница', 'Суббота')
        msg = bot.send_message(message.chat.id, 'Какой день недели тебе нужен?', reply_markup=week_markup)
        bot.register_next_step_handler(msg, handle_time_day)
    elif message.text.lower().strip() == 'неделя':
        resp = ''
        for day in days:
            resp += show_timetable(timetable, user_info, day)
        bot.send_message(message.chat.id, resp, reply_markup=user_markup)
    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Я не могу показать расписание. Период введён неправильно.')
        bot.register_next_step_handler(msg, handle_timetable)


def handle_time_day(message):
    day = message.text.lower().strip()
    if day in days:
        resp = show_timetable(timetable, user_info, day)
        bot.send_message(message.chat.id, resp, reply_markup=user_markup)
    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Я не могу показать расписание на этот день.')
        bot.register_next_step_handler(msg, handle_time_day)


def handle_materials(message):
    if materials['Дисциплина'].str.lower().isin([message.text.lower().strip()]).any():
        mats = materials[materials['Дисциплина'].str.lower() == message.text.lower().strip()][
            'Ссылка на материалы'].squeeze()
        bot.send_message(message.chat.id, f'Вот ссылка:\n{mats}', reply_markup=user_markup)
    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Таких материалов у меня нет.')
        bot.register_next_step_handler(msg, handle_materials)


def handle_formulas(message):
    if formulas['Дисциплины'].str.lower().isin([message.text.lower().strip()]).any():
        form = formulas[formulas['Дисциплины'].str.lower() == message.text.lower().strip()][
            'Формулы оценивания'].squeeze()
        bot.send_message(message.chat.id, f'Вот формула:\n{form}', reply_markup=user_markup)
    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Такой формулы у меня нет.')
        bot.register_next_step_handler(msg, handle_formulas)


def handle_deadlines(message):
    if message.text.lower().strip() == 'ближайший день':
        resp = get_deadlines('day')
        bot.send_message(message.chat.id, resp, reply_markup=user_markup)
    elif message.text.lower().strip() == 'ближайшая неделя':
        resp = get_deadlines('week')
        bot.send_message(message.chat.id, resp, reply_markup=user_markup)
    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Я не могу показать дедлайны. Период введён неправильно.')
        bot.register_next_step_handler(msg, handle_deadlines)


def handle_mark(message):
    if message.text.strip() in ('1', '2', '3', '4', '5'):
        review['mark'] = message.text.strip()
        msg = bot.send_message(message.chat.id, '''Спасибо за оценку!
Пожалуйста, напиши отзыв о работе бота.''')
        bot.register_next_step_handler(msg, handle_review)
    elif message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        msg = bot.send_message(message.chat.id, 'Эта оценка находится вне шкалы.')
        bot.register_next_step_handler(msg, handle_mark)


def handle_review(message):
    if message.text.lower().strip() == '/menu':
        msg = bot.send_message(message.chat.id, 'Какая информация тебе нужна?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, handle_options)
    else:
        bot.send_message(message.chat.id, '''Спасибо за отзыв!
Команда ФиПЛ-бота учтёт твои пожелания в будущем.''', reply_markup=user_markup)
        review['review'] = message.text
        reviews.loc[len(reviews.index)] = [review['mark'], review['review']]
        reviews.to_csv('reviews.csv', sep=';', index=False)


# @atexit.register
# def bot_goodbye():
#     bot.send_message(user_info['user_id'], 'Отключаюсь... Не теряйте!', reply_markup=user_markup)


bot.polling(none_stop=True)
