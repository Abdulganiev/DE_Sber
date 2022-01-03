def init_tables(connect):
	cursor = connect.cursor()
	
	cursor.execute('''
		CREATE TABLE if not exists customer(
			id integer primary key autoincrement,
			name varchar(128),
			age integer)
			''')

	cursor.execute('''
		CREATE TABLE if not exists product(
			id integer primary key autoincrement,
			title varchar(128),
			price integer)
			''')
	
	cursor.execute('''
		CREATE TABLE if not exists orders(
			id integer primary key autoincrement,
			customer_id integer,
			product_id integer)
			''')

def addCustomer(connect, name, age):
	cursor = connect.cursor()
	cursor.execute("""
		INSERT INTO customer (name, age) VALUES (?, ?)
		""", [name, age])
	print(f'{name} и {age} добавлены в customer')
	connect.commit()

def addProduct(connect, title, price):
	cursor = connect.cursor()
	cursor.execute("""
		INSERT INTO product (title, price) VALUES (?, ?)
		""", [title, price])
	print(f'{title} и {price} добавлены в product')
	connect.commit()

# def sale(connect, name, title):
#  	cursor = connect.cursor()
#  	cursor.execute("""
#  		INSERT INTO orders (customer_id, product_id) 
#  		   VALUES ((select id from customer where name=?), 
#  		           (select id from product where title=?))
#  		""", [name, title])
#  	connect.commit()

def sale(connect, name, title):
	cursor = connect.cursor()
	cursor.execute('select id from customer where name = ?', [name])
	n = cursor.fetchall()
	if len(n) == 0:
		print(f'пользователя с именем {name} нету')
		return
	else:
		customer_id = n[0][0]
		print(f'{n} добавлен в sale')

	cursor.execute('select id from product where title = ?', [title])

	n = cursor.fetchall()
	if len(n) == 0:
		print(f'товара с названием {title} нету')
		return
	else:
		product_id = n[0][0]
		print(f'{n} добавлен в sale')
 
	cursor.execute('''INSERT INTO orders (customer_id, product_id)
						VALUES (?, ?)''', [customer_id, product_id])
	connect.commit()


def drop_Tables(connect):
	cursor = connect.cursor()

	cursor.execute('drop table customer')
	cursor.execute('drop table product')
	cursor.execute('drop table orders')
	