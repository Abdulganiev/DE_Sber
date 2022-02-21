import os
import re
from datetime import datetime
import subprocess

def checking_files():
    '''Функция проверки наличия все необходимых файлов,которые необходимы для начала 
       обработки данных, старт будет только тогда когда соберутся все три файла '''
    files = []
    path = os.getcwd()
    cnt = 0
    c = os.listdir(os.chdir(os.getcwd()+r'/data'))
    for file in c:
        if re.findall(r'^transactions_', file) and file.endswith(".txt"):
            files.append(file)
            cnt += 1
        if re.findall(r'^terminals_', file) and file.endswith(".xlsx"):
            files.append(file)
            cnt += 1
        if re.findall(r'^passport_blacklist_', file) and file.endswith(".xlsx"):
            files.append(file)
            cnt += 1
    os.chdir(path)
    text = ','.join(files)
    if cnt > 0:
        writing_to_log_file( '%s собраны в каталоге' % (text))
        return files
    else:
        writing_to_log_file('Файлов нет')
        return files

def programs_start():
    '''функция начала работы программы, переносит из data файлы в корень программы,
       которые необходимы для начала обработки данных, старт будет только тогда когда соберутся все три файла'''
    files = []
    path = os.getcwd()
    c = os.listdir(os.chdir(os.getcwd()+r'/data'))
    for file in c:
        if re.findall(r'^transactions_', file) and file.endswith(".txt"):
            files.append(file)
            os.replace(file, path + '/' + file)
        if re.findall(r'^terminals_', file) and file.endswith(".xlsx"):
            files.append(file)
            os.replace(file, path + '/' + file)
        if re.findall(r'^passport_blacklist_', file) and file.endswith(".xlsx"):
            files.append(file)
            os.replace(file, path + '/' + file)
    os.chdir(path)
    if len(files) > 0:
        text = ','.join(files)
        writing_to_log_file( '%s готовы к обработке' %(text))
    return files

def writing_to_log_file(text):
    '''функция создания лог файла и записи в него информации'''
    dt = datetime.now().strftime('%Y-%m-%d %X')
    log_file = re.sub('\W', '_', datetime.now().strftime('%Y-%m-%d')) + '.log'
    path = 'log/' + log_file
    print(text)
    with open(path, 'a+') as file_log:
        file_log.write(dt + ' : ' + text + '\n')

def programs_end(file):
    '''функция для перемещения файлов в archive и их архивирование'''
    
    path = 'archive/' + file
    # перенос
    os.replace(file, path)
    writing_to_log_file(file + ' перенесен в archive')
    # архивирование
    # subprocess.call(['bzip2', '-f' , path])
    writing_to_log_file(file + ' заархивирован')

def return_file(file):
    os.replace(file, r'data/' + file)
    writing_to_log_file(file + ' перенесен обратно в каталог data')
    return 0