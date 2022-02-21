import pandas as pd
from file_scripts import *


#****************************************************************************************************
def drop_sq_tranc(conn, sq):
    '''Функция для удаления счетчика'''
    cursor = conn.cursor()
    try:
        cursor.execute('DROP SEQUENCE %s' % (sq))
        writing_to_log_file('Счетчик %s удален' % (sq))
    except:
        writing_to_log_file('ошибка SEQUENCE')


#****************************************************************************************************
def drop_table(conn, table):
    '''функция удаления таблицы'''
    cursor = conn.cursor()
    try:
        cursor.execute('DROP TABLE %s' % (table))
        writing_to_log_file('Таблица %s удалена' % (table))
    except:
        writing_to_log_file('Ошибка удаления таблицы %s' % (table))


#****************************************************************************************************
# Раздел функций для терминалов
#****************************************************************************************************
def init_terminals(conn):
    '''Функкция для создания исторической таблицы terminals_hist'''
    cursor = conn.cursor()
    table = 'de1h.s_00_dwh_dim_terminals_hist'
    try:
        cursor.execute(
            '''CREATE TABLE %s (
                id number(10) not null,
                terminal_id varchar(20) not null,
                terminal_type varchar(20) not null,
                terminal_city varchar(128) not null,
                terminal_address varchar(128) not null,
                effective_from date DEFAULT sysdate,
                effective_to date DEFAULT to_date('31.12.2999,23:59:59','dd.mm.yyyy,hh24:mi:ss'),
                deleted_flg integer DEFAULT 0,
                CONSTRAINT check_deleted_flg  CHECK(deleted_flg in (0, 1)),
                PRIMARY KEY (id)
                )''' % (table)
                )
        writing_to_log_file('%s создана' % (table))
    except:
        writing_to_log_file('Ошибка создания %s' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))
    try:
        cursor.execute('CREATE SEQUENCE de1h.s_00_sq_terminals_hist START WITH 1')
        writing_to_log_file('Создан SEQUENCE s_00_sq_terminals_hist')
    except:
        writing_to_log_file('Ошибка создания SEQUENCE s_00_sq_terminals_hist')

#****************************************************************************************************
def init_stg_terminals(conn):
    '''Функкция для создания таблицы stg_terminals и загрузки в нее данных'''
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_terminals'
    drop_table(conn, table)
    try:
        cursor.execute(
            '''CREATE TABLE %s 
                (terminal_id varchar(128),
                 terminal_type varchar(128),
                 terminal_city varchar(128),
                 terminal_address varchar(128))
                ''' % (table)
                )
        writing_to_log_file('%s создана' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table))
        cursor.execute('SELECT count(*) FROM %s' % (table))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('в %s %s записей' % (table, cnt))

#****************************************************************************************************
def insert_table_terminals(conn, file):
    '''функция загрузки данных из файла terminals.xlsx'''
    df = pd.read_excel(file, header=0, index_col=None)
    writing_to_log_file(file + 'загружен в датафрейм')
    
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_terminals'
    cursor.executemany('''INSERT INTO %s (
        terminal_id, terminal_type, terminal_city, terminal_address) 
        VALUES (trim(?), trim(?), ?, ?)''' % (table), df.values.tolist())
    cursor.execute('SELECT count(*) FROM %s' % (table))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('Данные загружены в %s, загружено %s записей' % (table, cnt))

#****************************************************************************************************
def new_terminals(conn):
    '''Функция для обработки данных о новых терминалах'''
    cursor = conn.cursor()
    table = 'de1h.s_00_stg_terminals'
    table_new = 'de1h.s_00_stg_new_terminals'
    table_hist = 'de1h.s_00_dwh_dim_terminals_hist'
    drop_table(conn, table_new)
    try:
        cursor.execute(
        '''CREATE TABLE %s as -- table_new
             SELECT
                t1.terminal_id,
                t1.terminal_type,
                t1.terminal_city,
                t1.terminal_address
              FROM %s t1 -- table
                   left join %s t2 -- table_hist
                on t1.terminal_id = t2.terminal_id
                WHERE t2.terminal_id is null''' % (table_new, table, table_hist)
                )
        cursor.execute('SELECT count(*) FROM %s' % (table_new))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('%s создана, загружено %s записей'  % (table_new, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table_new))

#****************************************************************************************************    
def delete_terminals(conn):
    '''Функция для обработки данных об удаленных терминалах'''
    cursor = conn.cursor()
    table_del = 'de1h.s_00_stg_del_terminals'
    table_hist = 'de1h.s_00_dwh_dim_terminals_hist'
    table = 'de1h.s_00_stg_terminals'
    drop_table(conn, table_del)
    try:
        cursor.execute(
        '''CREATE TABLE %s AS -- table_del
             SELECT
                t1.terminal_id,
                t1.terminal_type,
                t1.terminal_city,
                t1.terminal_address
              FROM %s t1 -- table_hist
                   left join %s t2 -- table
                on t1.terminal_id = t2.terminal_id
                WHERE t2.terminal_id is null and 
                      t1.effective_to = to_date('31.12.2999,23:59:59','dd.mm.yyyy,hh24:mi:ss') and
                      t1.deleted_flg = 0
                ''' % (table_del, table_hist, table)
                )
        cursor.execute('SELECT count(*) FROM %s' % (table_del))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('%s создана, загружено %s записей' % (table_del, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table_del))

#****************************************************************************************************
def chenge_terminals(conn):
    '''Функция для обработки данных об измененных терминалах'''
    cursor = conn.cursor()
    table_chenge = 'de1h.s_00_stg_chenge_terminals'
    table_hist = 'de1h.s_00_dwh_dim_terminals_hist'
    table = 'de1h.s_00_stg_terminals'
    drop_table(conn, table_chenge)
    try:
        cursor.execute(
        '''CREATE TABLE %s as -- table_chenge
             SELECT
                t1.terminal_id,
                t1.terminal_type,
                t1.terminal_city,
                t1.terminal_address
              FROM %s t1 -- table
                   inner join %s t2 -- table_hist
                on t1.terminal_id = t2.terminal_id and
                   t2.effective_to = to_date('31.12.2999,23:59:59','dd.mm.yyyy,hh24:mi:ss') and
                   (t1.terminal_id != t2.terminal_id or
                    t1.terminal_type != t2.terminal_type or
                    t1.terminal_city != t2.terminal_city or
                    t1.terminal_address != t2.terminal_address)''' % (table_chenge, table, table_hist)
                    )
        cursor.execute('SELECT count(*) FROM %s' % (table_chenge))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('%s создана, загружено %s записей' % (table_chenge, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table_chenge))

#****************************************************************************************************
def chenge_terminals_hist(conn):
    '''Функция загрузки данных в основную таблицу терминалов de1h.s_00_dwh_dim_terminals_hist'''
    cursor = conn.cursor()
    table = 'de1h.s_00_dwh_dim_terminals_hist'
    table_chenge = 'de1h.s_00_stg_chenge_terminals'
    table_del = 'de1h.s_00_stg_del_terminals'
    table_new = 'de1h.s_00_stg_new_terminals'

    writing_to_log_file('Загрузка данных в основную таблицу терминалов %s' % (table))
    
    # обновление поля effective_to для записей на основании таблицы изменений терминалов de1h.s_00_stg_chenge_terminals
    cursor.execute('''
        UPDATE %s-- table
            SET effective_to = sysdate - INTERVAL '1' SECOND
            WHERE terminal_id in (SELECT terminal_id FROM %s) -- table_chenge
                and effective_to = to_date('2999-12-31,23:59:59', 'yyyy.mm.dd,hh24:mi:ss')
                ''' % (table, table_chenge)
                )
    cursor.execute('SELECT count(*) FROM %s' % (table_chenge))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('поля effective_to для записей %s обновлены на основании %s, обновлено %s записей' % (table, table_chenge, cnt))
    
    # обновление поля effective_to для записей на основании таблицы удаления терминалов de1h.s_00_stg_del_terminals
    cursor.execute('''
        UPDATE %s -- table
            SET effective_to = sysdate - INTERVAL '1' SECOND
            WHERE terminal_id in (SELECT terminal_id FROM %s) -- table_del
                and effective_to = to_date('2999-12-31,23:59:59', 'yyyy.mm.dd,hh24:mi:ss')
                ''' % (table, table_del)
                )
    cursor.execute('SELECT count(*) FROM %s' % (table_del))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('поля effective_to для записей %s обновлены на основании %s, обновлено %s записей' % (table, table_del, cnt))

    # загрузка новый записей в de1h.s_00_dwh_dim_terminals_hist из de1h.s_00_stg_new_terminals
    cursor.execute(''' 
        INSERT INTO %s -- table
            (id,
            terminal_id,
            terminal_type,
            terminal_city,
            terminal_address
            )
        SELECT de1h.s_00_sq_terminals_hist.nextval,
            terminal_id,
            terminal_type,
            terminal_city,
            terminal_address
        from %s -- table_new
        ''' % (table, table_new)
        )
    cursor.execute('SELECT count(*) FROM %s' % (table_new))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('%s записи обновлены на основании %s, обновлено %s записей' % (table, table_new, cnt))

    # загрузка новый записей в de1h.s_00_dwh_dim_terminals_hist из de1h.s_00_stg_chenge_terminals
    cursor.execute(''' 
        INSERT INTO %s -- table
            (id,
            terminal_id,
            terminal_type,
            terminal_city,
            terminal_address
            )
        SELECT de1h.s_00_sq_terminals_hist.nextval,
            terminal_id,
            terminal_type,
            terminal_city,
            terminal_address
        from %s -- table_chenge
        ''' % (table, table_chenge)
        )
    cursor.execute('SELECT count(*) FROM %s' % (table_chenge))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('%s записи обновлены на основании %s, обновлено %s записей' % (table, table_chenge, cnt))

    # загрузка новый записей в de1h.s_00_dwh_dim_terminals_hist из de1h.s_00_stg_del_terminals с флагом удаления
    cursor.execute(''' 
        INSERT INTO %s -- table
            (id,
            terminal_id,
            terminal_type,
            terminal_city,
            terminal_address,
            deleted_flg 
            )
        SELECT de1h.s_00_sq_terminals_hist.nextval,
            terminal_id,
            terminal_type,
            terminal_city,
            terminal_address,
            1
        from %s -- table_del
        ''' % (table, table_del)
        )
    cursor.execute('SELECT count(*) FROM %s' % (table_del))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('%s записи обновлены на основании %s, обновлено %s записей' % (table, table_del, cnt))
