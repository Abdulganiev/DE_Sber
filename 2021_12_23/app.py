import sqlite3

connect = sqlite3.connect('sber_2.db')
cursor = connect.cursor()

cursor.execute("""
 	CREATE TABLE if not exists product(
 		id integer primary key autoincrement,
 		title varchar(128),
 		price integer,
 		start_dttm datetime default current_timestamp,
 		end_dttm datetime default (datetime('2999-12-31 23:59:59'))
 		)""")

def addRow(title, price):
	cursor.execute("""
		 select count(*) 
		   from product 
		   where title = ? and
		   	     price = ? and
		         end_dttm = datetime('2999-12-31 23:59:59')""", [title, price])
	n = cursor.fetchall()
	if len(n) != 0:
	 	print(f'товар {title} уже есть')
	 	return
	cursor.execute("""
		UPDATE product 
			set end_dttm = datetime('now', '-1 second')
		where title = ? and
		      end_dttm = datetime('2999-12-31 23:59:59')
		      """, [title])
	cursor.execute('INSERT INTO product (title, price) VALUES (?, ?)', [title, price])
	connect.commit()

addRow('ролики1', 4000)
addRow('ролики2', 2000)
addRow('ролики3', 3000)

def showTable(tableName):
	print('_-'*20)
	print(tableName)
	print('_-'*20)
	cursor.execute(f'SELECT * from {tableName}')
	for row in cursor.fetchall():
		print(row)
	print('_-'*20)

showTable('product')
