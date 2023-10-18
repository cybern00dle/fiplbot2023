import datetime
import httplib2
import locale
import pandas as pd
import time

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from fipl_data import formulas, materials, minors, students, timetable, client_secret


def register_user(df, user_id, user_name):
    if not df['user_id'].isin([user_id]).any():
        df.loc[len(df.index)] = [user_id, user_name]
        df.to_csv(f'users.csv', sep=';', index=False)


def authorize_user(df, user_id):
    return df[df['user_id'] == user_id]['name'].squeeze()


def read_user_info(df, user_info):
    user_row = df[df['ФИО'].str.lower() == user_info['name']]
    user_info['group'] = user_row['Академическая группа'].squeeze()
    user_info['language'] = user_row['Язык'].squeeze()
    user_info['nis1'] = user_row['НИС'].squeeze()
    user_info['nis2'] = user_row['НИС2'].squeeze()


def show_timetable(df, user_info, period):
    time_df = df[df['День недели'].str.lower() == period]
    opts = ['21ФПЛ1, 21ФПЛ2', user_info['group'], user_info['language'], user_info['nis1'], user_info['nis2']]
    message = f'\n{period.upper()}\n'
    for i, row in time_df.iterrows():
        if time_df.at[i, 'группа'] in opts:
            disc = time_df.at[i, 'Дисциплина']
            time = time_df.at[i, 'Время']
            corp = time_df.at[i, 'Корпус']
            au = time_df.at[i, 'Аудитория']
            info = ', '.join([disc, time, corp, au])
            message += info
            message += '\n'
    if message == f'\n{period.upper()}\n':
        message += 'Нет занятий'
    message += '\n'
    return message


def get_deadlines(period):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        client_secret, 'https://www.googleapis.com/auth/calendar.readonly')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    locale.setlocale(locale.LC_TIME, 'ru_RU')

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    now_day = round(time.time()) + 86400
    now_day = datetime.datetime.fromtimestamp(now_day).isoformat() + 'Z'
    now_week = round(time.time()) + 604800
    now_week = datetime.datetime.fromtimestamp(now_week).isoformat() + 'Z'

    if period == 'day':
        events_result = service.events().list(
            calendarId='tegzestkij@gmail.com', timeMin=now, timeMax=now_day,
            maxResults=100, singleEvents=True,
            orderBy='startTime').execute()
        deadlines = events_result.get('items', [])
    else:
        events_result = service.events().list(
            calendarId='tegzestkij@gmail.com', timeMin=now, timeMax=now_week,
            maxResults=100, singleEvents=True,
            orderBy='startTime').execute()
        deadlines = events_result.get('items', [])

    if not deadlines:
        return 'Нет событий на заданный период.'
    else:
        msg = 'События на заданный период:\n\n'
        for deadline in deadlines:
            try:
                dd_desc = deadline['description']
            except KeyError:
                dd_desc = 'Нет описания.'

            dd_title = deadline['summary']
            dd_start_gen = deadline['start'].get('dateTime')
            dd_dt = datetime.datetime.strptime(dd_start_gen, '%Y-%m-%dT%H:%M:%S+03:00')
            dd_start = dd_dt.strftime('%A, htt1%d %b %Y, %H:%M')

            msg += f'{dd_title}\n{dd_start}\n{dd_desc}\n\n'
        return msg
