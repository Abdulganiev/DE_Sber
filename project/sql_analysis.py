from file_scripts import *
from sql_terminals import drop_table


#****************************************************************************************************
# Раздел функций для анализа
#****************************************************************************************************

def drop_view(conn, view):
    '''Функция удаления представления'''
    cursor = conn.cursor()
    try:
        cursor.execute('''DROP VIEW %s''' % (view))
        writing_to_log_file('Представление %s удален' % (view))
    except:
        writing_to_log_file('Ошибка удаления представления %s' % (view))

#****************************************************************************************************
def init_view_bank(conn):
    '''Функция создания представления для данных таблиц из схемы bank'''
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE OR REPLACE VIEW de1h.s_00_v_bank AS
            SELECT
            t1.LAST_NAME||' '||t1.FIRST_NAME||' '||t1.PATRONYMIC as FIO,
            t1.DATE_OF_BIRTH,
            t1.PASSPORT_NUM,
            t1.PASSPORT_VALID_TO,
            t1.PHONE,
            trim(t3.CARD_NUM) as card_num,
            t2.VALID_TO as account_valid_to
            FROM bank.clients t1
                 inner join bank.accounts t2
              ON t1.CLIENT_ID =  t2.CLIENT and t1.UPDATE_DT is null and t2.UPDATE_DT is null
                 inner join bank.cards t3
              ON t2.ACCOUNT = t3.ACCOUNT and t3.UPDATE_DT is null
                    ''')
        writing_to_log_file('Представление s_00_v_bank создано или обновлено')
    except:
        writing_to_log_file('Представление s_00_v_bank либо уже создано или ошибка')

#****************************************************************************************************
def init_view_transactions(conn):
    '''Функция создания представления для транзакций + терминалы'''
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE OR REPLACE VIEW de1h.s_00_v_transactions AS    
            SELECT 
            t1.TRANS_ID,
            t1.trans_data,
            trim(t1.card_num) as card_num,
            t1.oper_type,
            t1.oper_result,
            t2.terminal_city,
            t2.effective_from,
            t2.effective_to,
            t2.deleted_flg
            FROM de1h.s_00_dwh_fact_transactions t1
                 inner join de1h.s_00_dwh_dim_terminals_hist t2
              ON t1.terminal = t2.terminal_id and
                 (--t1.trans_data between t2.effective_from and t2.effective_to or
                  t1.trans_data between to_date('2021-03-01 00:00:00', 'YYYY-MM-DD hh24:mi:ss') and t2.effective_to)
                    ''')
        writing_to_log_file('Представление s_00_v_transactions создано или обновлено')
    except:
        writing_to_log_file('Представление s_00_v_transactions либо уже создано или ошибка')

#****************************************************************************************************
def init_data_showcase(conn):
    '''Функция по созданию таблицы витрины данных'''
    cursor = conn.cursor()
    table = 'de1h.s_00_rep_fraud'
    try:
        cursor.execute('''
        CREATE TABLE %s (
                id number(10) not null,
                event_dt date not null,
                passport varchar(128) not null,
                fio varchar(128) not null,
                phone varchar(128) not null,
                event_type varchar(128) not null,
                report_dt date not null,
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
        cursor.execute('CREATE SEQUENCE de1h.s_00_sq_rep_fraud START WITH 1')
        writing_to_log_file('Создан SEQUENCE s_00_sq_rep_fraud')
    except:
        writing_to_log_file('Ошибка создания SEQUENCE s_00_sq_rep_fraud')


#****************************************************************************************************
def init_v_stg_data_showcase(conn):
    '''Функция по созданию представления для отбора данных для витрины'''
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE OR REPLACE VIEW de1h.s_00_v_stg_rep_fraud AS
SELECT *
FROM
(SELECT 
    t1.next_trans_data as event_dt,
    t2.passport_num as passport,
    t2.fio,
    t2.phone,
    'Совершение операций в разных городах в течение одного часа' as event_type,
    sysdate as report_dt
from
(SELECT 
    trans_data,
    card_num,                
    terminal_city as city,
    lead(card_num) OVER (partition by card_num order by trans_data) as next_card_num,
    lead(terminal_city) OVER (partition by card_num order by trans_data) as next_city,
    lead(trans_data) OVER (partition by card_num order by trans_data) as next_trans_data
FROM de1h.s_00_v_transactions) t1
     inner join de1h.s_00_v_bank t2
  ON t1.card_num = t2.card_num       
WHERE (t1.next_trans_data - t1.trans_data)*24 < 1 and
      t1.CARD_NUM = t1.next_card_num and t1.city != t1.next_city 
UNION
SELECT 
    t1.trans_data as event_dt,
    t2.passport_num as passport,
    t2.fio,
    t2.phone,
    'Совершение операции при просроченном паспорте' as event_type,
    sysdate as report_dt
from de1h.s_00_v_transactions t1
     INNER JOIN de1h.s_00_v_bank t2
  ON t1.card_num = t2.card_num
WHERE (t2.passport_valid_to + 1) < t1.trans_data
UNION
SELECT 
t1.trans_data as event_dt,
    t2.passport_num as passport,
    t2.fio,
    t2.phone,
    'Совершение операции при невалидном аккаунте' as event_type,
    sysdate as report_dt
from de1h.s_00_v_transactions t1
     INNER JOIN de1h.s_00_v_bank t2
  ON t1.card_num = t2.card_num
WHERE t1.trans_data > (t2.account_valid_to + 1)
UNION
SELECT 
    t1.trans_data as event_dt,
    t2.passport_num as passport,
    t2.fio,
    t2.phone,
    'Совершение операции при заблокированном паспорте' as event_type,
    sysdate as report_dt
from de1h.s_00_v_transactions t1
     INNER JOIN de1h.s_00_v_bank t2
  ON t1.card_num = t2.card_num
     INNER JOIN de1h.s_00_dwh_fact_blcklst t3
  ON t2.PASSPORT_NUM = t3.PASSPORT_NUM
WHERE (t3.DATA + 1) <= t1.trans_data)
                ''')
        writing_to_log_file('de1h.s_00_v_stg_rep_fraud создана')
    except:
        writing_to_log_file('Ошибка создания de1h.s_00_v_stg_rep_fraud')


#****************************************************************************************************

def init_new_data_showcase(conn):
    '''Функция загрузки новый данных в таблицу витрины данных'''
    cursor = conn.cursor()
    table = 'de1h.s_00_v_stg_rep_fraud'
    table_new = 'de1h.s_00_stg_new_rep_fraud'
    table_hist = 'de1h.s_00_rep_fraud'
    drop_table(conn, table_new)
    try:
        cursor.execute(
        '''CREATE TABLE de1h.s_00_stg_new_rep_fraud as -- table_new
             SELECT * FROM
                (SELECT
                  event_dt, 
                  passport, 
                  fio, 
                  phone, 
                  event_type                 
                FROM de1h.s_00_v_stg_rep_fraud
                minus
                SELECT
                  event_dt, 
                  passport, 
                  fio, 
                  phone, 
                  event_type                 
                FROM de1h.s_00_rep_fraud)
                ''')
        cursor.execute('SELECT count(*) FROM %s' % (table_new))
        cnt = cursor.fetchone()[0]
        writing_to_log_file('%s создана, загружено %s записей'  % (table_new, cnt))
    except:
        writing_to_log_file('Ошибка создание %s' % (table_new))
    

#****************************************************************************************************

def insert_data_showcase(conn):
    '''Функция загрузки новый данных в таблицу витрины данных'''
    cursor = conn.cursor()
    table_hist = 'de1h.s_00_rep_fraud'
    table_new = 'de1h.s_00_stg_new_rep_fraud'
    cursor.execute(''' 
        INSERT INTO %s -- table
            (id,
             event_dt,
             passport,
             fio,
             phone,
             event_type,
             report_dt
            )
        SELECT de1h.s_00_sq_rep_fraud.nextval,
             event_dt, 
             passport, 
             fio, 
             phone, 
             event_type, 
             sysdate
        from %s -- table_new
        ''' % (table_hist, table_new)
        )
    cursor.execute('SELECT count(*) FROM %s' % (table_new))
    cnt = cursor.fetchone()[0]
    writing_to_log_file('%s записи обновлены на основании %s, обновлено %s записей' % (table_hist, table_new, cnt))






    pass
