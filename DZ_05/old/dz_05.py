import sqlite3
from def_dz_05 import *

connect = sqlite3.connect('DZ_05.db')
cursor = connect.cursor()



print_help()

n = -1
while n != 0:
	n = int(input('? (9 - помощь) - '))
	if n == 1: # создать таблицу Users
		creating_table(connect)
	elif n == 9:
		print_help()
	elif n == 2: # добавить пользователя в таблицу Users указав его данные
		first_name, last_name, age, salary = input('Введите Имя, Фамилию, Возраст и зарплату через пробел - ').split(' ')
		addUser(connect,first_name, last_name, int(age), int(salary))
	elif n == 3: # удалить пользователя
		first_name, last_name = input('Введите Имя и Фамилию через пробел - ').split(' ')
		deleteUser(connect, first_name, last_name)
	elif n == 4: #сохранить данные о пользователях на указанную дату в csv файл
		#file_path = input('Укажите путь до файла - ')
		d = input('Введите дату в виде гггг-мм-дд - ')
		saveUserToCSV(connect, d)
	elif n == 5:
		showTables(connect)
	elif n == 6:
		delTableUsers(connect)
	elif n == 7:
		print_tables(connect)
