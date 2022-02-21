import sqlite3
import pandas as pd


connect = sqlite3.connect('sber.db')
cursor = connect.cursor()


def csv2sql(path_to_file, tableName):
	df = pd.read_csv(path_to_file)
	df.to_sql(tableName, con = connect, if_exists='replace')


def init():
	cursor.execute(''' 
		CREATE TABLE if not exists auto_hist(
			id integer primary key autoincrement,
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
			deleted_flg integer check(deleted_flg in (0, 1)) default 0,
			start_dttm datetime default current_timestamp,
			end_dttm datetime default (datetime('2999-12-31 23:59:59'))
		)
	''')


# сформировать таблицу с записями, которые есть в auto_tmp, но отсутствуют в auto_hist (по auto_key)

def newRows():
	cursor.execute(''' 
		CREATE TABLE new_rows_tmp as
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
			left join auto_hist t2
			on t1.auto_key = t2.auto_key
			where t2.auto_key is null
	''')


def deletedRows():
	cursor.execute(''' 
		CREATE TABLE deleted_rows_tmp as
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
			on t1.auto_key = t2.auto_key
			where t2.auto_key is null
	''')

def deletedRows():
	cursor.execute(''' 
		CREATE TABLE changed_rows_tmp as
			select
				t1.model,
				t1.transmission,
				t1.body_type,
				t1.drive_type,
				t1.color,
				t1.production_year,
				t1.engine_capacity,
				t1.horsepower,
				t1.engine_type,
				t1.price,
				t1.milage
			from auto_tmp t1
			inner join auto_hist t2
			on t1.auto_key = t2.auto_key
			and (  t1.model <> t2.model
				or t1.transmission <> t2.transmission
				or t1.body_type <> t2.body_type
				or t1.drive_type <> t2.drive_type
				or t1.color <> t2.color
				or t1.production_year <> t2.production_year
				or t1.engine_capacity <> t2.engine_capacity
				or t1.horsepower <> t2.horsepower
				or t1.engine_type <> t2.engine_type
				or t1.price <> t2.price
				or t1.milage <> t2.milage
			)
	''')


def showSource(sourceName):
	print('_-'*20)
	print(sourceName)
	print('_-'*20)

	cursor.execute(f'select * from {sourceName}')
	for row in cursor.fetchall():
		print(row)

	print('_-'*20+'\n')

# csv2sql("store/data.csv", 'auto_tmp')
# showSource('auto_tmp')

init()