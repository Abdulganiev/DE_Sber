import pandas as pd
from file_scripts import *
from sql_terminals import drop_table


#****************************************************************************************************
# Раздел функций для транзаций
#****************************************************************************************************
def init_transactions(conn):
    '''Функкция для создания исторической таблицы s_00_dwh_fact_transactions'''
    cursor = conn.cursor()
    table = 'de1h.s_00_dwh_fact_transactions'

    try:
        cursor.execute(
            '''CREATE TABLE %s (
                id number(10) not null,
                trans_id int not null,
                trans_data date not null,
                amount number(12,2) not null,
                card_num varchar(128) not null,
                oper_type varchar(128) not null,
                oper_result varchar(128) not null,
                terminal varchar(128) not null,
                create_dt date DEFAULT sysdate,
                update_dt date,
                PRIMARY KEY (id, trans_id)
                )''' % (table)
                )
        writing_to_log_file('%s создана' % (table))
    except:
        writing_to_log_file('Ошибка создания %s' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))

    try: # создание счетчика для таблицы s_00_dwh_fact_transactions
        cursor.execute('CREATE SEQUENCE de1h.s_00_sq_transactions START WITH 1')
        writing_to_log_file('Создан SEQUENCE s_00_sq_transactions')
    except:
        writing_to_log_file('Ошибка создания SEQUENCE s_00_sq_transactions')

#****************************************************************************************************
def init_stg_transactions(conn):
    '''Функкция для создания таблицы s_00_stg_transactions'''
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_transactions'
    drop_table(conn, table)
    try:
        cursor.execute(
            '''CREATE TABLE %s (
                trans_id int not null,
                trans_data date not null,
                amount number(12,2) not null,
                card_num varchar(128) not null,
                oper_type varchar(128) not null,
                oper_result varchar(128) not null,
                terminal varchar(128) not null
                )''' % (table)
                )
        writing_to_log_file('%s создана' % (table))
    except:
        writing_to_log_file('Ошибка создания %s' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))

#****************************************************************************************************
def insert_table_transactions(conn, file):
    '''функция загрузки данных из файла transactions.xlsx'''
    df = pd.read_csv(file, sep=';')
    df['transaction_date'] = df['transaction_date'].astype(str)
    writing_to_log_file(file + ' загружен в датафрейм')

    cursor = conn.cursor()
    table = 'de1h.s_00_stg_transactions'
    try:
        cursor.executemany('''INSERT INTO %s 
                (trans_id, trans_data, amount, card_num, oper_type, oper_result, terminal) 
            VALUES (?, to_date(?, 'YYYY-MM-DD hh24:mi:ss'), ?, trim(?), ?, ?, ?)''' % (table), df.values.tolist())
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('Данные загружены в %s, загружено %s записей' % (table, cnt))
    except:
        writing_to_log_file('!!! Ошибка загрузки данных в %s из датафрейм' % (table))
        # return return_file(file)


#****************************************************************************************************
def new_transactions(conn):
    '''Функция для обработки данных о новых транзакциях, необходима для исключения повторной загрузки'''
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_transactions'
    table_new = 'de1h.s_00_stg_new_transactions'
    table_hist = 'de1h.s_00_dwh_fact_transactions'
    drop_table(conn, table_new)
    try:
        cursor.execute(
        '''CREATE TABLE %s as -- table_new
             SELECT
                t1.trans_id,
                t1.trans_data,
                t1.amount,
                t1.card_num,
                t1.oper_type,
                t1.oper_result,
                t1.terminal
              FROM %s t1 -- table
                   left join %s t2 -- table_hist
                on t1.trans_id = t2.trans_id
                WHERE t2.trans_id is null''' % (table_new, table, table_hist)
                )
        cursor.execute('SELECT count(*) FROM %s' % (table_new))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('%s создана, загружено %s записей'  % (table_new, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table_new))

#****************************************************************************************************
def chenge_transactions_hist(conn):
    '''Функция загрузки данных в основную таблицу s_00_dwh_fact_transactions'''
    cursor = conn.cursor()
    table = 'de1h.s_00_dwh_fact_transactions'
    table_new = 'de1h.s_00_stg_new_transactions'

    writing_to_log_file('Загрузка данных в основную таблицу %s' % (table))
    
    # загрузка новый записей в s_00_dwh_fact_transactions из s_00_stg_new_transactions
    cursor.execute(''' 
        INSERT INTO %s -- table
            (id,
            trans_id,
            trans_data,
            amount,
            card_num,
            oper_type,
            oper_result,
            terminal
            )
        SELECT de1h.s_00_sq_transactions.nextval,
            trans_id,
            trans_data,
            amount,
            card_num,
            oper_type,
            oper_result,
            terminal
        from %s -- table_new
        ''' % (table, table_new)
        )
    cursor.execute('SELECT count(*) FROM %s' % (table_new))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('%s записи обновлены на основании %s, обновлено %s записей' % (table, table_new, cnt))
