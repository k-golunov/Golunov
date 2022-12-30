import sqlite3

import pandas as pd
import math

# Задаем основные настройки и считываем файлы
pd.set_option("display.max_columns", None)
# df_currencies = pd.read_csv("currencies.csv")
data = {"name": [], "salary": [], "area_name": [], "published_at": []}
currency = ['RUR', 'USD', 'KZT', 'BYR', 'UAH', 'EUR']
df = pd.read_csv("vacancies_dif_currencies.csv")


# Основной цикл, перебираем весь файл
for index, row in df.iterrows():
    # для создания файла на 100 строк
    if len(data['name']) >= 100:
        break
    # выделяем основные переменные
    salary_from = row["salary_from"]
    salary_to = row["salary_to"]
    value_curr = row["salary_currency"]
    # данные, не требующие обработки
    if math.isnan(salary_from) and math.isnan(salary_to):
        continue
    if value_curr not in currency:
        continue
    # Получаем коэффициент для перевода в ррубли
    if value_curr != 'RUR':
        date = row["published_at"]
        date = date[:7]
        # получаем коэффициент из бд
        try:
            sqlite_connection = sqlite3.connect('Database_3_5_1.db')
            cursor = sqlite_connection.cursor()
            sqlQuery = f"""SELECT {value_curr} FROM task_3_5_1 WHERE date = ?"""
            cursor.execute(sqlQuery, (date,))
            kk = cursor.fetchall()
            k = float(kk[0][0])
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
            k = 1

        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                # print("Соединение с SQLite закрыто")
    else:
        k = 1
    if math.isnan(salary_from) or math.isnan(salary_to):
        if math.isnan(salary_from):
            data["salary"].append(salary_to * k)
        else:
            data["salary"].append(salary_from * k)
    else:
        data["salary"].append(((salary_from + salary_to) / 2) * k)

    # Заполняем данные
    data["name"].append(row["name"])
    data["area_name"].append(row["area_name"])
    data["published_at"].append(row["published_at"])

# Сохраняем в csv
new_df = pd.DataFrame(data)
try:
    sqlite_connection = sqlite3.connect('Database_3_5_1.db')
    new_df.to_sql('task_3_5_2', sqlite_connection, if_exists='replace', index=False)

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

finally:
    if (sqlite_connection):
        sqlite_connection.close()
