import pandas as pd
import re
from datetime import datetime
import sqlite3

def print_help():
	help_prog = {
    '1': 'создать таблицу Users',
    '2': 'добавить пользователя в таблицу Users указав его данные',
    '3': 'удалить пользователя',
    '4': 'сохранить данные о пользователях на указанную дату в csv файл',
    '5': 'cписок таблиц',
    '6': 'начать с начала (удалить таблицы)',
    '7': 'вывести содержимое таблицы',
    '0': 'выход из программы'
	}
	print('Выберите, что хотите выполнить: ')
	for key, value in help_prog.items():
		print(f'{key} - {value}')


def creating_table(connect):
	"""Функция, которая создает таблицу users. Если она уже есть, то необходимо вывести об этом сообщение в консоль"""
	cursor = connect.cursor()

	try: # таблица пользователей
		cursor.execute('''
			CREATE TABLE users(
	 			user_id integer PRIMARY KEY autoincrement,
 				first_name varchar(128) NOT NULL, 
		 		last_name varchar(128) NOT NULL, 
 				age integer NOT NULL, 
 				salary integer NOT NULL,
 				deleted_flg integer CHECK(deleted_flg in (0, 1)) default 0,
 				start_dttm datetime DEFAULT current_timestamp,
		 		end_dttm datetime DEFAULT (datetime('2999-12-31 23:59:59'))
		 		)
				''')
		print('Таблица "Users" создана')
	except sqlite3.OperationalError as e:
		if str(e) == 'table users already exists':
			return print('Таблица "Users" была создана ранее')	
		print(e)
		
def addUser(connect, first_name, last_name, age, salary):
	"""добавить запись о пользователе
		1. запись должна добавляться в историческую таблицу (с полями start_dttm, end_dttm)
		2. параметры пользователя: имя, фамилия, возраст, зарплата
		3. если пользователь с таким ИМЕНЕМ и ФАМИЛИЕЙ уже есть, то новая запись считается актуальной версией информации о пользователе
	"""
	cursor = connect.cursor()

	cursor.execute("""
		UPDATE users 
 		SET end_dttm = datetime('now', '-1 second')
		WHERE first_name = ? and last_name = ? and end_dttm = datetime('2999-12-31 23:59:59')
		     """ , [first_name, last_name])

	cursor.execute("""
		INSERT INTO users (first_name, last_name, age, salary) VALUES (?, ?, ?, ?)
		    """, [first_name, last_name, age, salary]
		    )

	connect.commit()

def deleteUser(connect, first_name, last_name):
	"""логически удалить пользователя (по имени и фамилии)"""

	cursor.execute("""
	select first_name, last_name, age, salary 
	from users 
	where first_name = ? and last_name = ? 
	      and end_dttm = datetime('2999-12-31 23:59:59')
	      and deleted_flg = 0
	""" , [first_name, last_name])

	last = cursor.fetchone()

	if last == None:
		return

	cursor.execute("""
		UPDATE users 
 		SET end_dttm = datetime('now', '-1 second')
		WHERE first_name = ? and last_name = ? and end_dttm = datetime('2999-12-31 23:59:59')
		     """ , [first_name, last_name])

	cursor.execute("""
		INSERT INTO users (first_name, last_name, age, salary, deleted_flg) 
		VALUES (?, ?, ?, ?, ?)
		    """, [*last, 1])

	connect.commit()

def saveUserToCSV(connect, d):
	"""сохранить данные о пользователях на указанную дату в csv файл 
		(если дата неуказана, то вывести данные на момент вызова функции)"""

	if len(d) == 0:
		d = datetime.now().strftime('%Y-%m-%d %X')

	sql = f"""
		select 
			first_name, 
			last_name, 
			age, 
			salary, 
			deleted_flg,
			start_dttm,
			end_dttm
	from users 
	where datetime('{d}') between date(start_dttm) and date(end_dttm)"""
	df = pd.read_sql(sql, con=connect)

	file_name = re.sub('\W', '_', d) + '.csv'

	df.to_csv(file_name, index=False)

def showTables(connect):
	cursor = connect.cursor()
	cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
	print('Список таблиц:')
	for row in cursor.fetchall():
	 	print(row[0])

def delTableUsers(connect):
	"""Функция удаления таблиц"""
	cursor = connect.cursor()
	try:	
		cursor.execute('DROP TABLE users')
		print('Таблица Users удалена')
	except:
		print('Таблицы Users еще не создана')

def print_tables(connect):
	"""Функция вывода содержимого таблиц"""
	cursor = connect.cursor()
	try:
		cursor.execute('SELECT * FROM users')
		print('Содержимое таблицы Users:')
		for row in cursor.fetchall():
		 	print(*row, sep=', ')
	except:
		print('Таблицы "Users" нет')
