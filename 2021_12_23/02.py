import sqlite3

connect = sqlite3.connect('sber.db')
cursor = connect.cursor()

cursor.execute("""
 	CREATE TABLE if not exists product(
 		id integer primary key autoincrement,
 		title varchar(128),
 		price integer,
 		deleted_flg integer check(deleted_flg in (0, 1)) default 0
 		)""")

cursor.execute("""
 	CREATE view if not exists v_product as 
 		select id, title, price 
 		 from product
 		 where deleted_flg = 0 
 		""")


def addRow(title, price):
	cursor.execute('INSERT INTO product (title, price) VALUES (?, ?)', [title, price])
	connect.commit()

# addRow('ролики1', 40000)
# addRow('ролики2', 20000)
# addRow('ролики3', 30000)

def showTable(tableName):
	print(tableName)
	cursor.execute(f'SELECT * from {tableName}')
	for row in cursor.fetchall():
		print(row)

showTable('v_product')

def deleteRow(id):
	cursor.execute("""
		UPDATE product 
		set deleted_flg=1
		where id = ?
		""", [id])
	connect.commit()

def recoverRow(id):
	cursor.execute("""
		UPDATE product 
		set deleted_flg=0
		where id = ?
		""", [id])
	connect.commit()

def updatePrice(id, price):
	cursor.execute("""
		UPDATE product 
		set price=?
		where id = ?
		""", [price, id])
	connect.commit()

updatePrice(3, 200)

#deleteRow(3)

#showTable('v_product')

# recoverRow(1)
# recoverRow(3)

showTable('v_product')
