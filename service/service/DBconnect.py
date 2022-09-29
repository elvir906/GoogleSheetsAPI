import os
from datetime import datetime as dt

import psycopg2
import telegram

from googlesheet import GSheets
from rubrate import GetRate
from settings import DATABASES

DB_NAME = DATABASES.get('default').get('NAME')
USER = DATABASES.get('default').get('USER')
PASSWORD = DATABASES.get('default').get('PASSWORD')
HOST = DATABASES.get('default').get('HOST')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_massge(bot, message):
    """Здесь бот отправляет сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        print(f'Сообщение {message} отправлено в Telegram')
    except Exception as error:
        print(f'Ошибка {error}. Бот не доступен')


def delivery_date_checking(date):
    """Проверка истечения срока поставки."""
    delivery_date = dt.strptime(date, '%d.%m.%Y')
    return dt.today() > delivery_date


def data_transfer():
    """
    Метод для переброски данных с листа гугл-таблицы в базу Postgres.
    Так же здесь реализована инициализации сверки даты поставки и
    отправки сообщения телеграм-ботом.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    sheet = GSheets()
    message = ''

    if sheet.check_changes():
        rate = GetRate().fetch_currency_rate()
        query_values = []
        sheet_values = []
        try:
            connection = psycopg2.connect(
                database=DB_NAME,
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=5432
            )
            cursor = connection.cursor()
            cursor.execute('TRUNCATE Orders')
            for item in reversed(range(len(sheet.get_values()))):
                sheet_values = sheet.get_values()[item]

                date_in_sheet = sheet_values[3]
                order_number_in_sheet = sheet_values[1]

                if delivery_date_checking(date_in_sheet):
                    message += f'№ {order_number_in_sheet} - {date_in_sheet};\n'

                sheet_values.insert(3, round(rate * float(sheet_values[2]), 2))
                query_values = [item, *sheet_values]
                query = 'INSERT INTO Orders (table_row_index, table_row_number, order_number, cost_usd, cost_rub, delivery_date) VALUES (%s, %s, %s, %s, %s, %s)'
                db_values = tuple(query_values)
                cursor.execute(query, db_values)

            connection.commit()
            count = cursor.rowcount
            print(count, 'Record inserted successfully into mobile table')

            if message != '':
                bot.send_message(
                    TELEGRAM_CHAT_ID,
                    'Истёк срок поставки заказа(-ов):\n' + message
                )

        except (Exception, psycopg2.Error) as error:
            print('Failed to insert record into mobile table:', error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')
    else:
        print('No changes was found')
