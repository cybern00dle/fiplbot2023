import pandas as pd

formulas = pd.read_csv('formulas.csv', sep=';')
materials = pd.read_csv('materials.csv', sep=';')
minors = pd.read_csv('minors.csv', sep=';')
students = pd.read_csv('students.csv', sep=';')
timetable = pd.read_csv('timetable.csv', sep=';')
reviews = pd.read_csv('reviews.csv', sep=';')
users = pd.read_csv('users.csv', sep=';')

client_secret = 'client_secret.json'

faq = '''Часто возникающие вопросы и проблемы при использовании бота.

Q: Почему бот медленно работает?
A: Бот написан при помощи библиотеки PyTelegramBotAPI, которая является синхронной. К сожалению, синхронные боты не предназначены для использования большим количеством пользователей одновременно, поэтому ответы бота могут задерживаться. В будущем возможна реализация бота через асинхронный aiogram.

Q: Бот показывает не моё персональное расписание/ссылку на майнор/etc. Что делать?
A: Проблема возникает из-за синхронности бота. Быстро решается командой /reset.

Q: Почему бот не понимает команду /menu при вводе ФИО?
A: Это сделано для того, чтобы процесс авторизации не прерывался и не было сбоев при смене ФИО пользователя.

Нет ответа на твой вопрос? Сообщи о проблеме разработчику: @ruadhseinneadairriordan'''
