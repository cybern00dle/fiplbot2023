import pandas as pd

from fipl_data import formulas, materials, minors, students, timetable


def read_user_info(df, user_info):
    user_row = df[df['ФИО'].str.lower() == user_info['name']]
    user_info['group'] = user_row['Академическая группа'].squeeze()
    user_info['language'] = user_row['Язык'].squeeze()
    user_info['nis1'] = user_row['НИС'].squeeze()
    user_info['nis2'] = user_row['НИС2'].squeeze()


def show_timetable(df, user_info, period):
    timetable = df[df['День недели'].str.lower() == period]
    opts = ['21ФПЛ1, 21ФПЛ2', user_info['group'], user_info['language'], user_info['nis1'], user_info['nis2']]
    message = f'\n{period.upper()}\n'
    for i, row in timetable.iterrows():
        if timetable.at[i, 'группа'] in opts:
            disc = timetable.at[i, 'Дисциплина']
            time = timetable.at[i, 'Время']
            corp = timetable.at[i, 'Корпус']
            au = timetable.at[i, 'Аудитория']
            info = ', '.join([disc, time, corp, au])
            message += info
            message += '\n'
    message += '\n'
    return message


def show_materials():
    pass
