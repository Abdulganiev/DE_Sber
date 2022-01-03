import sqlite3
import pandas as pd

connect = sqlite3.connect('day28.db')
cursor = connect.cursor()

def pd_print(path):
	df = pd.read_csv(path)
	# print(df.head(10))


def sql2sql(path, tableName):
	df = pd.read_csv(path)
	# print(df.head(10))
	df.to_sql(tableName, con = connect, if_exists = 'replace')

def print_table(table):
	#Функция вывода содержимого таблицы auto_tmp
	cursor = connect.cursor()
	cursor.execute(f'SELECT * FROM {table}')
	print('_-'*20)
	print(f'Содержимое таблицы {table}:')
	for row in cursor.fetchall():
	 	print(*row, sep=', ')
	print('_-'*20)

def showTables():
	cursor = connect.cursor()
	cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
	print('_-'*20)
	print('Список таблиц:')
	for row in cursor.fetchall():
	 	print(row[0])
	print('_-'*20)	 	

def delTableUsers(connect):
	"""Функция удаления таблиц"""
	cursor = connect.cursor()
	try:	
		cursor.execute('DROP TABLE auto_tmp')
		print('Таблица auto_tmp удалена')
	except:
		print('Таблицы auto_tmp еще не создана')
	# try:
	# 	cursor.execute('DROP TABLE salarys')
	# 	print('Таблица Salarys удалена')
	# except:
	# 	print('Таблицы Salarys еще не создана')	 	

def init():
	cursor.execute('''
		CREATE TABLE if not exists auto_hist(
		id integer PRIMARY KEY autoincrement,
		model varchar(128),
		transmission varchar(128),
		body_type varchar(128),
		drive_type varchar(128),
		color varchar(128),
		production_year integer,
		auto_key integer,
		engine_capacity real, 
		horsepower integer,
		engine_type varchar(128),
		price integer,
		milage integer,
		deleted_flg integer CHECK(deleted_flg in (0, 1)) default 0,
		start_dttm datetime DEFAULT current_timestamp,
		end_dttm datetime DEFAULT (datetime('2999-12-31 23:59:59'))
		)
		''')

def newRows():
	cursor.execute('''
		CREATE TABLE if not exists new_rows_tmp as
			select 
				-- t1.id,
				t1.model,
				t1.transmission,
				t1.body_type,
				t1.drive_type,
				t1.color,
				t1.production_year,
				t1.auto_key,
				t1.engine_capacity, 
				t1.horsepower,
				t1.engine_type,
				t1.price,
				t1.milage 
			from auto_tmp t1 
			     left join auto_hist t2
			     on t1.auto_key=t2.auto_key
			where t2.auto_key is null
		''')

def deletedRows():
	cursor.execute('''
		CREATE TABLE if not exists del_rows_tmp as
			select 
					t1.model,
					t1.transmission,
					t1.body_type,
					t1.drive_type,
					t1.color,
					t1.production_year,
					t1.auto_key,
					t1.engine_capacity, 
					t1.horsepower,
					t1.engine_type,
					t1.price,
					t1.milage 
			from auto_hist t1 
			     left join auto_tmp t2
			     on t1.auto_key=t2.auto_key
			where t2.auto_key is null and t1.end_dttm datetime = ('2999-12-31 23:59:59')
		''')

# сформировать функцию, которая создает таблицу с измененными данными
def chengedRows():
	cursor.execute('''
		CREATE TABLE if not exists chenged_rows_tmp as
			select 
				t1.model,
				t1.transmission,
				t1.body_type,
				t1.drive_type,
				t1.color,
				t1.production_year,
				t1.auto_key,
				t1.engine_capacity, 
				t1.horsepower,
				t1.engine_type,
				t1.price,
				t1.milage
			from auto_tmp t1
			     inner join auto_hist t2
			     on t1.auto_key=t2.auto_key and
			     	(t1.model <> t2.model
					or t1.transmission <> t2.transmission
					or t1.body_type <> t2.body_type
					or t1.drive_type <> t2.drive_type
					or t1.color <> t2.color
					or t1.production_year <> t2.production_year
					or t1.engine_capacity <> t2.engine_capacity
					or t1.horsepower <> t2.horsepower
					or t1.engine_type <> t2.engine_type
					or t1.price <> t2.price
					or t1.milage <> t2.milage)
		''')

def chengedAutoHist():
		cursor.execute("""
		UPDATE auto_hist 
			set end_dttm = datetime('now', '-1 second')
		where auto_key in (select auto_key from chenged_rows_tmp)
		      and
		      end_dttm = datetime('2999-12-31 23:59:59')
		      """)

		cursor.execute("""
		UPDATE auto_hist 
			set end_dttm = datetime('now', '-1 second')
		where auto_key in (select auto_key from del_rows_tmp)
		      and
		      end_dttm = datetime('2999-12-31 23:59:59')
		      """)

		cursor.execute("""
		INSERT INTO auto_hist(model, transmission, body_type, drive_type, color, 
							  production_year, engine_capacity, horsepower, engine_type, price, milage)
		SELECT model, transmission, body_type, drive_type, color, 
			   production_year, engine_capacity, horsepower, engine_type, price, milage
		FROM new_rows_tmp
 	    """)

		cursor.execute("""
		INSERT INTO auto_hist(model, transmission, body_type, drive_type, color, 
							  production_year, engine_capacity, horsepower, engine_type, price, milage)
		SELECT model, transmission, body_type, drive_type, color, 
			   production_year, engine_capacity, horsepower, engine_type, price, milage
		FROM chenged_rows_tmp
 	    """)

		cursor.execute("""
		INSERT INTO auto_hist(model, transmission, body_type, drive_type, color, 
							  production_year, engine_capacity, horsepower, engine_type, price, milage, deleted_flg)
		SELECT model, transmission, body_type, drive_type, color, 
			   production_year, engine_capacity, horsepower, engine_type, price, milage, 1
		FROM del_rows_tmp
 	    """)


# sql2sql('data.csv', 'auto_tmp')

showTables()

# print_table('auto_tmp')

#init()

newRows()

deletedRows()

chengedRows()
