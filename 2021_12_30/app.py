import sqlite3
import json

def addClient(connect, name, lastname, age):
    #Функция, которая добавляет клиентов в таблицу (если клиента с такими фамилией и именем нет в таблице)
	cursor = connect.cursor()
	cursor.execute('select count(*) from client where lower(name) = lower(?) and lower(lastname) = lower(?)', [name, lastname])
		
	if cursor.fetchone()[0] != 0:
		return print(f'Клиент {name} {lastname} уже есть в таблице')
	
	cursor.execute("""
			INSERT INTO client (name, lastname, age) VALUES (?, ?, ?)
				""", [name, lastname, age])
	print(f'{name} {lastname} {age} добавлен в таблицу')
	connect.commit()

def init(connect):
	#Функция, которая создает таблицу client если она ежу есть, необходимо вывести об этом сообщение в консоль
	cursor = connect.cursor()
	
	try:
		cursor.execute('''
			CREATE TABLE client(
				id integer primary key autoincrement,
				name varchar(128),
				lastname varchar(128),
				age integer)
				''')
	except sqlite3.OperationalError as e:
		print(str(e))
		return print('Таблица "Client" была создана ранее')

def init2(connect):
	cursor = connect.cursor()
	cursor.execute('SELECT count(*) FROM sqlite_master WHERE type = "table" and name = "client" ')

	if cursor.fetchone()[0] > 0:
		return print('Таблица "Client" была создана ранее')
	cursor.execute('''
			CREATE TABLE client(
				id integer primary key autoincrement,
				name varchar(128),
				lastname varchar(128),
				age integer)
				''')		

def print_table(connect, nameTable):
	#Функция вывода содержимого таблицы с клиентами
	cursor = connect.cursor()
	cursor.execute(f'SELECT * FROM {nameTable}')
	print(f'Содержимое таблицы {nameTable}:')
	for row in cursor.fetchall():
	 	print(*row, sep=', ')

def addClientJSON(connect, file_path):
    #Функция, которая получив путь до JSON файла и добавляет клиентов в таблицу
	#(только тех, которые по фамилии и имени отсутствуют в таблице)"""
	with open(file_path, 'r', encoding='utf-8') as f:
		text = json.load(f)
	for line in text:
		addClient(connect, **line)	 	

def avgClient(connect):
	#Функция, которая возвращает средний возраст клиентов
	cursor = connect.cursor()
	cursor.execute('SELECT round(avg(age), 2) FROM client')
	print('Cредний возраст клиентов -', cursor.fetchone()[0])



# from def_dz_04 import *

connect = sqlite3.connect('sber30.db')
cursor = connect.cursor()

#init(connect)
# init2(connect)

# addClient(connect, 'Вася', 'Пупкин', 32)

# addClientJSON(connect, 'clients.txt')


print_table(connect, 'client')

avgClient(connect)