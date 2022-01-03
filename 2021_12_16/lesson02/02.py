import sqlite3

from database import *

connect = sqlite3.connect('sber.db')
cursor = connect.cursor()

drop_Tables(connect)

init_tables(connect)

addCustomer(connect, 'Игорь', 33)
addCustomer(connect, 'Ольга', 41)
addCustomer(connect, 'Слава', 35)
addCustomer(connect, 'Сережа', 43)
addCustomer(connect, 'Евгений', 35)

addProduct(connect, 'Велосипед', 34000)
addProduct(connect, 'Ролики', 34400)
addProduct(connect, 'Лыжи', 34600)
addProduct(connect, 'Скейт', 34700)
addProduct(connect, 'Самокат', 34200)

sale(connect, 'Игорь', 'Самокат')
sale(connect, 'Игорь', 'Лыжи')
sale(connect, 'Игорь', 'Лыжи')
sale(connect, 'Сережа', 'Лыжи')
sale(connect, 'Сережа', 'Танк')
sale(connect, 'Серж', 'Танк')


cursor.execute('SELECT * FROM customer')
print()
print('вывод таблицы customer')
for el in cursor.fetchall():
	print(el)

print('_-'*20)
print('_-'*20)
print('_-'*20)

cursor.execute('SELECT * FROM product')
print('вывод таблицы product')
for el in cursor.fetchall():
	print(el)

print('_-'*20)
print('_-'*20)
print('_-'*20)

cursor.execute('SELECT * FROM orders')
print('вывод таблицы product')
for el in cursor.fetchall():
	print(el)
