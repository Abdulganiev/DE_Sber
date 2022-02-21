import jaydebeapi
from sql_terminals import *
from sql_transactions import *
from sql_passport import *
from sql_analysis import * 


conn = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver',
                          'jdbc:oracle:thin:de1h/bilbobaggins@de-oracle.chronosavant.ru:1521/deoracle',
                          ['de1h','bilbobaggins'],
                          'ojdbc7.jar')

if len(checking_files()) > 0: # если в папке data собраны все файлы, необходимые для обработки, то
    files = programs_start()
    for file in files:
        if 'transactions' in file:
            transactions = file
            init_transactions(conn) # создание основной таблицы s_00_dwh_fact_transactions
            init_stg_transactions(conn) # создание таблицы s_00_stg_transactions
            insert_table_transactions(conn, transactions) # загрузка данных в датафрейм и далее в
            new_transactions(conn) # создание таблицы s_00_stg_new_transactions
            chenge_transactions_hist(conn) # загрузка сведений в основную таблицу s_00_dwh_fact_blcklst
            programs_end(file)

        if 'terminals' in file:
            terminals = file
            init_terminals(conn) # создание основной таблицы s_00_dwh_dim_terminals_hist
            init_stg_terminals(conn) # создание первичной таблицы s_00_stg_terminals для загрузки данных о терминалов
            insert_table_terminals(conn, terminals) # загрузка данных в датафрейм и далее в s_00_stg_terminals
            new_terminals(conn) # загрузка новый сведений во временную таблицу s_00_stg_new_terminals
            delete_terminals(conn) # загрузка сведений для удаления во временную таблицу s_00_stg_del_terminals
            chenge_terminals(conn) # загрузка сведений для удаления во временную таблицу s_00_stg_chenge_terminals
            chenge_terminals_hist(conn) # загрузка сведений в основную таблицу s_00_dwh_dim_terminals_hist
            programs_end(file)

        if 'passport' in file:
            passport = file
            init_passport(conn) # создание основной таблицы s_00_dwh_fact_blcklst
            init_stg_passport(conn) # создание таблицы s_00_stg_blcklst
            insert_table_passport(conn, passport) # загрузка данных в датафрейм и далее в s_00_stg_blcklst
            new_passport(conn) # создание таблицы s_00_stg_new_blcklst
            chenge_passport_hist(conn) # загрузка сведений в основную таблицу s_00_dwh_fact_blcklst
            programs_end(file)

    init_view_bank(conn) # создание представления по табллицам банка
    init_view_transactions(conn) # создание представления по таблицам терминала и транзакций
    init_data_showcase(conn) # создание таблицы витрины данных
    init_v_stg_data_showcase(conn) # создание представления для отбора данных для витрины данных
    init_new_data_showcase(conn)
    insert_data_showcase(conn)
        



# drop_table(conn, 'de1h.s_00_dwh_dim_terminals_hist') # для отладки
# drop_sq_tranc(conn, 'de1h.s_00_sq_terminals_hist') # для отладки
# drop_table(conn,'de1h.s_00_dwh_fact_blcklst') # для отладки
# drop_sq_tranc(conn, 'de1h.s_00_sq_blcklst') # для отладки
# drop_table(conn,'de1h.s_00_dwh_fact_transactions') # для отладки
# drop_sq_tranc(conn, 'de1h.s_00_sq_transactions') # для отладки
# drop_table(conn,'de1h.s_00_rep_fraud') # для отладки
# drop_sq_tranc(conn, 'de1h.s_00_sq_rep_fraud') # для отладки

