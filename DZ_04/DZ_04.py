import sqlite3

from def_dz_04 import *

connect = sqlite3.connect('dz_04.db')
cursor = connect.cursor()

print_help()

n = -1
while n != 0:
	n = int(input('? (9 - помощь) - '))
	if n == 1:
		creating_table(connect)
	elif n == 9:
		print_help()
	elif n == 2:
		name, lastname, age = input('Введите Имя, Фамилию и возраст через пробел - ').split(' ')
		addClient(connect, name, lastname, int(age))
	elif n == 3:
		file_path = input('Укажите путь до файла - ')
		addClientJSON(connect, file_path)
	elif n == 4:
		avgClient(connect)
	elif n == 5:
		print_table(connect)

