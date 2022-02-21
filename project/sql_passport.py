import pandas as pd
from file_scripts import *
from sql_terminals import drop_table


#****************************************************************************************************
# Раздел функций для паспартов
#****************************************************************************************************
def init_passport(conn):
    '''Функкция для создания исторической таблицы passport_blacklist_hist'''
    cursor = conn.cursor()
    table = 'de1h.s_00_dwh_fact_blcklst'

    try:
        cursor.execute(
            '''CREATE TABLE %s (
                id number(10) not null,
                data date not null,
                passport_num varchar(128) not null,
                create_dt date DEFAULT sysdate,
                update_dt date ,
                PRIMARY KEY (id, passport_num)
                )''' % (table)
                )
        writing_to_log_file('%s создана' % (table))
    except:
        writing_to_log_file('Ошибка создания %s' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))

    try: # Создание счетчика для таблицы s_00_dwh_fact_blcklst
        cursor.execute('CREATE SEQUENCE de1h.s_00_sq_blcklst START WITH 1')
        writing_to_log_file('Создан SEQUENCE s_00_sq_blcklst')
    except:
        writing_to_log_file('Ошибка создания SEQUENCE s_00_sq_blcklst')

#****************************************************************************************************
def init_stg_passport(conn):
    '''Функкция для создания таблицы s_00_stg_blcklst'''
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_blcklst'
    drop_table(conn, table)
    try:
        cursor.execute(
            '''CREATE TABLE %s (
                data date not null,
				passport_num varchar(128) not null
                )''' % (table)
                )
        writing_to_log_file('%s создана' % (table))
    except:
        writing_to_log_file('Ошибка создания %s' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))

#****************************************************************************************************
def insert_table_passport(conn, file):
    '''функция загрузки данных из файла passport_blacklist.xlsx'''
    df = pd.read_excel(file, header=0, index_col=None )
    df['date'] = df['date'].astype(str)
    writing_to_log_file(file + ' загружен в датафрейм')

    cursor = conn.cursor()
    table = 'de1h.s_00_stg_blcklst'
    cursor.executemany('''INSERT INTO %s 
    						(
        					data, 
        					passport_num
        					) 
        VALUES (to_date(?, 'YYYY-MM-DD'), trim(?) )''' % (table), df.values.tolist())
    cursor.execute('SELECT count(*) FROM %s' % (table))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('Данные загружены в %s, загружено %s записей' % (table, cnt))

#****************************************************************************************************
def new_passport(conn):
    '''Функция для обработки данных о новых паспартов, необходима для исключения повторной загрузки'''
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_blcklst'
    table_new = 'de1h.s_00_stg_new_blcklst'
    table_hist = 'de1h.s_00_dwh_fact_blcklst'
    drop_table(conn, table_new)
    try:
        cursor.execute(
        '''CREATE TABLE %s as -- table_new
             SELECT
                t1.data,
                t1.passport_num
              FROM %s t1 -- table
                   left join %s t2 -- table_hist
                on t1.passport_num = t2.passport_num
                WHERE t2.passport_num is null''' % (table_new, table, table_hist)
                )
        cursor.execute('SELECT count(*) FROM %s' % (table_new))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('%s создана, загружено %s записей'  % (table_new, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table_new))

#****************************************************************************************************
def chenge_passport_hist(conn):
    '''Функция загрузки данных в основную таблицу s_00_dwh_fact_blcklst'''
    cursor = conn.cursor()
    table = 'de1h.s_00_dwh_fact_blcklst'
    table_new = 'de1h.s_00_stg_new_blcklst'

    writing_to_log_file('Загрузка данных в основную таблицу %s' % (table))
    
    # загрузка новый записей в s_00_dwh_fact_blcklst из s_00_stg_new_blcklst
    cursor.execute(''' 
        INSERT INTO %s -- table
            (id,
            data,
            passport_num
            )
        SELECT de1h.s_00_sq_blcklst.nextval,
            data,
            passport_num
        from %s -- table_new
        ''' % (table, table_new)
        )
    cursor.execute('SELECT count(*) FROM %s' % (table_new))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('%s записи обновлены на основании %s, обновлено %s записей' % (table, table_new, cnt))
