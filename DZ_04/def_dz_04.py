import json


def print_help():
	help_prog = {
    '1': 'создать таблицу clien',
    '2': 'добавить клиента в таблицу в ручном режиме указав его данные',
    '3': 'добавляет клиентов в таблицу из JSON файла',
    '4': 'вывести средний возраст клиентов',
    '5': 'вывести содержимое таблицы',
    '0': 'выход из программы'
	}
	print('Выберите, что хотите выполнить:')
	for key, value in help_prog.items():
		print(f'{key} - {value}')

def creating_table(connect):
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
	except:
		return print('Таблица "Client" была создана ранее')


def addClient(connect, name, lastname, age):
    #Функция, которая добавляет клиентов в таблицу (если клиента с такими фамилией и именем нет в таблице)
	cursor = connect.cursor()
	cursor.execute('select id from client where lower(name) = lower(?) and lower(lastname) = lower(?)', [name, lastname])
	client_id = cursor.fetchall()
	
	if len(client_id) == 0:
		cursor.execute("""
			INSERT INTO client (name, lastname, age) VALUES (?, ?, ?)
				""", [name, lastname, age])
		print(f'{name} {lastname} {age} добавлен в таблицу')
		connect.commit()
	else:
		print(f'Клиент {name} {lastname} уже есть в таблице')
		return


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
	cursor.execute('SELECT avg(age) FROM client')
	return print('Cредний возраст клиентов -',round(cursor.fetchall()[0][0], 2))

def print_table(connect):
	#Функция вывода содержимого таблицы с клиентами
	cursor = connect.cursor()
	cursor.execute('SELECT * FROM client')
	print('Содержимое таблицы client:')
	for row in cursor.fetchall():
	 	print(*row, sep=', ')
