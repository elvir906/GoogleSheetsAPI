from datetime import datetime as dt

import psycopg2

from googlesheet import GSheets
from rubrate import GetRate
from settings import DATABASES

DB_NAME = DATABASES.get('default').get('NAME')
USER = DATABASES.get('default').get('USER')
PASSWORD = DATABASES.get('default').get('PASSWORD')
HOST = DATABASES.get('default').get('HOST')


def firstly_data_transfer():
    """
    Метод для переброски данных с листа гугл-таблицы в базу
    при первом запуске.
    """
    sheet = GSheets()

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
        count = 0
        cursor.execute('TRUNCATE Orders')

        for item in reversed(range(len(sheet.get_values()))):
            sheet_values = sheet.get_values()[item]

            sheet_values.insert(3, round(rate * float(sheet_values[2]), 2))
            query_values = [item, *sheet_values]
            query = 'INSERT INTO Orders (table_row_index, table_row_number, order_number, cost_usd, cost_rub, delivery_date) VALUES (%s, %s, %s, %s, %s, %s)'
            db_values = tuple(query_values)
            cursor.execute(query, db_values)
            count += cursor.rowcount

        connection.commit()
        print(count, 'Record inserted successfully into mobile table')

    except (Exception, psycopg2.Error) as error:
        print('Failed to insert record into mobile table:', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')
