import sqlite3
import pandas as pd
import re
from datetime import datetime

def init():
	"""Функция, которая создает таблицы users. Если они уже есть, то необходимо вывести об этом сообщение в консоль"""

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
		print(e)
		print('Таблица "Users" была создана ранее')

def addUser(first_name, last_name, age, salary):
	"""добавить запись о пользователе
		1. запись должна добавляться в историческую таблицу (с полями start_dttm, end_dttm)
		2. параметры пользователя: имя, фамилия, возраст, зарплата
		3. если пользователь с таким ИМЕНЕМ и ФАМИЛИЕЙ уже есть, то новая запись считается актуальной версией информации о пользователе
	"""
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

def print_table(nameTable):
	#Функция вывода содержимого таблицы с клиентами
	cursor.execute(f'SELECT * FROM {nameTable}')
	print(f'Содержимое таблицы {nameTable}:')
	for row in cursor.fetchall():
	 	print(*row, sep=', ')


def delTableUsers():
	"""Функция удаления таблиц"""
	try:	
		cursor.execute('DROP TABLE users')
		print('Таблица Users удалена')
	except:
		print('Таблицы Users еще не создана')


def deleteUser(first_name, last_name):
	"""логически удалить пользователя (по имени и фамилии)"""
	cursor.execute("""
	select first_name, last_name, age, salary 
	from users 
	where first_name = ? and last_name = ? 
	      and end_dttm = datetime('2999-12-31 23:59:59')
	      and deleted_flg = 0
	""" , [first_name, last_name])

	lasr = cursor.fetchone()

	# print(lasr)

	if lasr == None:
		return

	cursor.execute("""
		UPDATE users 
 		SET end_dttm = datetime('now', '-1 second')
		WHERE first_name = ? and last_name = ? and end_dttm = datetime('2999-12-31 23:59:59')
		     """ , [first_name, last_name])

	cursor.execute("""
		INSERT INTO users (first_name, last_name, age, salary, deleted_flg) 
		VALUES (?, ?, ?, ?, ?)
		    """, [*lasr, 1])

	connect.commit()

def saveUserToCSV(d):
	if len(d) == 0:
		d = datetime.now().strftime('%Y-%m-%d %X')
		# print(d)

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
	where datetime('{d}') between date(start_dttm) and date(end_dttm)
	"""

	# sql = 'select * from users'	

	# df = pd.read_sql('select * from users where datetime(?) between date(start_dttm) and date(end_dttm)', params = [d], con=connect)
	df = pd.read_sql(sql, con=connect)

	file_name = re.sub('\W', '_', d) + '.csv'

	print(file_name)

	df.to_csv(file_name, index=False)

	print(df)




connect = sqlite3.connect('sber30.db')
cursor = connect.cursor()

# delTableUsers()

# init()

# addUser('Вася', 'Пупкин',  28, 35012)

# deleteUser('Вася', 'Пупкин')

# deleteUser('Вася', 'Пупкин')

d = '2021-12-30 17:37:41	'

saveUserToCSV('')

print_table('users')