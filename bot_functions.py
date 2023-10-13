import pandas as pd

from fipl_data import formulas, materials, minors, students, timetable


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
    message += '\n'
    return message
