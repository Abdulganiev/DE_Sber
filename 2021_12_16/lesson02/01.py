import sqlite3

connect = sqlite3.connect('sber.db')
cursor = connect.cursor()

cursor.execute("""
 	CREATE TABLE if not exists product(
 		id integer,
 		title varchar(128),
 		price integer
 		)""")

def addProduct(id, title, price):
	cursor.execute("""
		INSERT INTO product (id, title, price) VALUES (?, ?, ?)
		""", [id, title, price])
	connect.commit()

def removeProduct(id):
	cursor.execute("""
 		DELETE from product
 			where id=?""", [id])
	connect.commit()

def chengePrice(id, price):
	cursor.execute("""
		UPDATE product set price=?
				where id=?""", [price, id])
	connect.commit()

def maxPrice():
	cursor.execute("""
		SELECT max(price)
		 FROM product
		""")
	return cursor.fetchone() #cursor.fetchall()[0][0]

#chengePrice(4, 107777)
#removeProduct(2)
#addProduct(7, 'ролики', 40000)

print(maxPrice())

# cursor.execute("""
# 	SELECT * FROM product
# 	""")

# for row in cursor.fetchall():
# 	print(row)

# for row in cursor.fetchall():
# 	print(row)