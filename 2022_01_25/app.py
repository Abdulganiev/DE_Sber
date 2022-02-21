import pandas as pd
import jaydebeapi


conn = jaydebeapi.connect(
	'oracle.jdbc.driver.OracleDriver',
	'jdbc:oracle:thin:de1h/bilbobaggins@de-oracle.chronosavant.ru:1521/deoracle',
	['de1h','bilbobaggins'],
	'ojdbc7.jar')


# https://www.oracle.com/database/technologies/jdbc-drivers-12c-downloads.html

curs = conn.cursor()


def addProduct(title, price):
	curs.execute('''
		INSERT INTO s01_product (id, title, price)
		VALUES (s01_product_sequence.nextval, ?, ?)
	''', [title, price]
	)
	curs.execute('select s01_product_sequence.nextval from dual')
	print(curs.fetchall())

def showTable():
	print('='*40)
	print('s01_product')
	print('_-'*20)
	curs.execute('select * from s01_product')
	for row in curs.fetchall():
		print(row)
	print('='*40)	

def create_sequence():
	try:
		curs.execute('CREATE SEQUENCE s01_product_sequence START WITH 1')
	except:
		print('Счетчик уже создан')

def drop_product():
	try:
		curs.execute('DROP TABLE s01_product')
		print('Таблица удалена')
		curs.execute('DROP SEQUENCE s01_product_sequence')
		print('Счетчик удален')
	except:
		print('ошибка')


def create_product():
	try:
		curs.execute("""
			CREATE TABLE s01_product(
				id integer primary key,
				title varchar(128),
				price number(6, 2)
			)
			""")
	except jaydebeapi.DatabaseError:
		print('Такая таблица уже есть')


# drop_product()

# create_sequence()
# create_product()

# drop_product()

addProduct('Мясо', 100.24)
showTable()