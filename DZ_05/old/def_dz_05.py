from datetime import datetime


def print_help():
	help_prog = {
    '1': 'создать таблицы',
    '2': 'добавить пользователя в таблицу Users указав его данные',
    '3': 'удалить пользователя',
    '4': 'сохранить данные о пользователях на указанную дату в csv файл',
    '5': 'cписок таблиц',
    '6': 'начать с начала (удалить таблицы)',
    '7': 'вывести содержимое таблиц',
    '8': 'вывести информацию по пользователю',
    '0': 'выход из программы'
	}
	print('Выберите, что хотите выполнить: ')
	for key, value in help_prog.items():
		print(f'{key} - {value}')


def creating_table(connect):
	"""Функция, которая создает таблицы users и salarys. Если они уже есть, то необходимо вывести об этом сообщение в консоль"""
	cursor = connect.cursor()

	try: # таблица пользователей
		cursor.execute('''
			CREATE TABLE users(
	 			user_id integer PRIMARY KEY autoincrement,
 				first_name varchar(128) NOT NULL, 
		 		last_name varchar(128) NOT NULL, 
 				age integer NOT NULL, 
 				deleted_flg integer CHECK(deleted_flg in (0, 1)) default 0)
				''')
		print('Таблица "Users" создана')
	except:
		print('Таблица "Users" была создана ранее')

	try: # таблица зарплат пользователей
		cursor.execute('''
			CREATE TABLE salarys(
	 			salary_id integer PRIMARY KEY autoincrement,
	 			user_id REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
		 		salary integer NOT NULL,
 				start_dttm datetime DEFAULT current_timestamp,
		 		end_dttm datetime DEFAULT (datetime('2999-12-31 23:59:59')))
				''')
		print('Таблица "Salarys" создана')
	except:
		print('Таблица "Salarys" была создана ранее')




def addUser(connect, first_name, last_name, age, salary):
	"""добавить запись о пользователе
		1. запись должна добавляться в историческую таблицу (с полями start_dttm, end_dttm)
		2. параметры пользователя: имя, фамилия, возраст, зарплата
		3. если пользователь с таким ИМЕНЕМ и ФАМИЛИЕЙ уже есть, то новая запись считается актуальной версией информации о пользователе
	"""
	cursor = connect.cursor()
	cursor.execute("""
		 SELECT count(*) 
		   FROM users t1 INNER JOIN salarys t2
		   ON t1.user_id = t2.user_id and 
		      t1.first_name = ? and t1.last_name = ? and
		   	  t1.age = ? and t2.salary = ? and
		         end_dttm = datetime('2999-12-31 23:59:59')""", [first_name, last_name, age, salary])
	n = cursor.fetchall()[0][0]
	if n != 0:
		print(f'пользователь {first_name} {last_name} с такими данными уже есть')
		return
	
	cursor.execute("""
		UPDATE salarys 
 			SET end_dttm = datetime('now', '-1 second')
			WHERE end_dttm = datetime('2999-12-31 23:59:59') and 
      			  user_id = 
       				(select user_id from users
          				where first_name = ? and last_name = ?)
		      """, [first_name, last_name])

	cursor.execute('SELECT count(user_id) FROM users WHERE first_name = ? and last_name = ? and age = ?', [first_name, last_name, age])
	n = cursor.fetchall()[0][0]

	if n == 0:
		cursor.execute('INSERT INTO users (first_name, last_name, age) VALUES (?, ?, ?)', [first_name, last_name, age])
		connect.commit()

	cursor.execute('SELECT user_id FROM users WHERE first_name = ? and last_name = ? and age = ?', [first_name, last_name, age])
	user_id = cursor.fetchall()[0][0]

	cursor.execute('INSERT INTO salarys (user_id, salary) VALUES (?, ?)', [user_id, salary])
	connect.commit()

def deleteUser(connect, first_name, last_name):
	"""логически удалить пользователя (по имени и фамилии)"""
	cursor = connect.cursor()
	cursor.execute("""
		UPDATE users 
		set deleted_flg=1
		where first_name = ? and last_name = ?
		""", [first_name, last_name])
	connect.commit()

def saveUserToCSV(connect, d):
	"""сохранить данные о пользователях на указанную дату в csv файл 
		(если дата неуказана, то вывести данные на момент вызова функции)
	"""
	if len(d) == 0:
		d = datetime.now().strftime('%Y-%m-%d')

	cursor = connect.cursor()
	cursor.execute("""
	select 
		t1.first_name, 
		t1.last_name, 
		t1.age, 
		t2.salary, 
		t1.deleted_flg,
		date(t2.start_dttm),
		date(t2.end_dttm)
	from users t1 inner join salarys t2
    	on t1.user_id = t2.user_id
	where ? between date(t2.start_dttm) and date(t2.end_dttm)
	""", [d])
	out = cursor.fetchall()
	# out1 = out.split(',')
	print(out)

	# with open("out.csv", 'w') as file_out:
	# 	expanded_text = ''
	# 	for row in out:
	# 		stroka = ''
	# 		for el in row:
	# 			stroka += str(el) + ';'
	# 		expanded_text += stroka + '\n'
	# 	print(expanded_text)
	# 	file_out.write(expanded_text)




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
	try:
		cursor.execute('DROP TABLE salarys')
		print('Таблица Salarys удалена')
	except:
		print('Таблицы Salarys еще не создана')

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
	try:
		cursor.execute('SELECT * FROM salarys')
		print('Содержимое таблицы Salarys:')
		for row in cursor.fetchall():
		 	print(*row, sep=', ')
	except:
		print('Таблицы "Salarys" нет')

def showUser(connect,first_name, last_name, age):
	
	pass
	