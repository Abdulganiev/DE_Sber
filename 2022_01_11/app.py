import sqlite3
import json
import pandas as pd
import re

con = sqlite3.connect('sber.db')
cursor = con.cursor()


def init():
	cursor.execute(''' 
		CREATE TABLE if not exists employees(
			name varchar(128), 
			lastname  varchar(128), 
			age integer, 
			salary integer, 
			deleted_flg integer default 0, 
			start_dttm datetime default current_timestamp, 
			end_dttm datetime default (datetime('2999-12-31 23:59:59'))
		)
	''')

def addEmployee(name, lastname, age, salary):
	cursor.execute(''' 
		UPDATE employees
		set end_dttm = datetime('now', '-1 second')
		where name = ? and lastname = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [name, lastname])

	cursor.execute('''
		INSERT INTO employees (name, lastname, age, salary)
		VALUES (?, ?, ?, ?)
	''', [name, lastname, age, salary])

	con.commit()



def deleteEmployee(name, lastname):
	cursor.execute('''select 
		name,
		lastname,
		age,
		salary
	 from employees
	 where name = ?
	 and lastname = ?
	 and end_dttm = datetime('2999-12-31 23:59:59')
	 and deleted_flg = 0
	''', [name, lastname])

	last_employee = cursor.fetchone()

	if last_employee == None:
		return

	cursor.execute(''' 
		UPDATE employees
		set end_dttm = datetime('now', '-1 second')
		where name = ? and lastname = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [name, lastname])

	cursor.execute('''
		INSERT INTO employees (name, lastname, age, salary, deleted_flg)
		VALUES (?, ?, ?, ?, ?)
	''', [*last_employee, 1])

	con.commit()

# 1) написать функцию, которая выгружает все данные из employees в csv файл
# 2) добавить аргумент в loadCSVfromSQL дата, на которую мы формируем выгрузку.


def loadCSVfromSQL(dttm='now'):
	df = pd.read_sql('''
		select 
			name,
			lastname,
			age,
			salary
		from employees 
		where datetime(?) between start_dttm and end_dttm
		and deleted_flg = 0''', 
					  params=[dttm], con=con)

	file_name = re.sub(r'\W', '_', dttm) + '.csv'
	df.to_csv(file_name, index=False)






def showTable(tableName):
	print('='*40)
	print(tableName)
	print('_-'*20)
	cursor.execute(f'select * from {tableName}')
	for row in cursor.fetchall():
		print(row)
	print('='*40)




# init()
# deleteEmployee('Гайк', 'Инанц')
# showTable('employees')


loadCSVfromSQL()
