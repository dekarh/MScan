# -*- coding: utf-8 -*-

#
# Загрузка базы фирм из excel
#

from mysql.connector import MySQLConnection, Error
from datetime import datetime
import openpyxl
from openpyxl import Workbook

from libScan import l, s, read_config, norm_phone, append_words, propusk

dbconfig = read_config(section='mysql')
exlconfig = read_config(section='excel_input')

wb = openpyxl.load_workbook(read_only=True, **exlconfig)
sheet = wb[wb.sheetnames[0]]

dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

print('\n\n', datetime.strftime(datetime.now(), "%H:%M:%S"), 'Начинаем импорт из excel в БД')
# read_cursor.execute('SELECT * FROM main WHERE inn >-1;')
# rows = read_cursor.fetchall()


row = []
for i, row in enumerate(sheet.rows):
    if i == 0:
        continue
    id = l(row[0].value)
    id_fil = l(row[1].value)
    name_words = []                                 # tuple для таблицы ключевых слов
    n_words = []
    name = s(row[2].value)
    full_name = s(row[3].value)
    append_words(name,n_words)
    append_words(full_name,n_words)
    for n in n_words:
        is_skip = False
        for p in propusk:
            if p[len(p) - 1:] == '%':
                if n.lower().startswith(p[:len(p)-1]):
                    is_skip = True
                    break
            else:
                if n.lower() == p:
                    is_skip = True
                    break
        if not is_skip:
            name_words.append((id, n))
    if len(s(row[4].value).upper().split(',')) < 2:
        address = s(row[4].value).upper() + ', ' + s(row[5].value).upper() + ', ' + s(row[6].value).upper()
    else:
        address = 'АСТРАХАНСКАЯ ОБЛ, ' + s(row[4].value).upper().split(',')[1] + ', ' + \
                  s(row[4].value).upper().split(',')[0] + ', '+ s(row[5].value).upper() + ', ' + s(row[6].value).upper()

    contacts = []                                   # tuple для таблицы контактов (телефоны тоже добавляем в контакты)
    phones_all = []                                 # tuple для таблицы телефонов
    mob = row[7].value
    if str(type(mob)) == "<class 'str'>":
        for phone in mob.split(';'):
            if norm_phone(phone) != None:
                phones_all.append((id, 'мобильный', norm_phone(phone)))
                contacts.append((id, 'мобильный', s(norm_phone(phone))))
    no_mob = row[8].value
    if str(type(no_mob)) == "<class 'str'>":
        for phone in no_mob.split(';'):
            if norm_phone(phone) != None:
                phones_all.append((id, 'стационарный', norm_phone(phone)))
                contacts.append((id, 'мобильный', s(norm_phone(phone))))
    fax = row[9].value
    if str(type(fax)) == "<class 'str'>":
        for phone in fax.split(';'):
            if norm_phone(phone) != None:
                phones_all.append((id, 'факс', norm_phone(phone)))
                contacts.append((id, 'мобильный', s(norm_phone(phone))))

    wwws = row[10].value
    if str(type(wwws)) == "<class 'str'>":
        for www in wwws.split('|'):
            if s(www) != '':
                contacts.append((id, 'www', s(www)))
    emails = row[11].value
    if str(type(emails)) == "<class 'str'>":
        for email in emails.split(','):
            if s(email) != '':
                contacts.append((id, 'e-mail', s(email)))
    socset = row[12].value
    if str(type(socset)) == "<class 'str'>":
        if s(socset) != '':
            contacts.append((id, 'facebook', s(socset)))
    socset = row[13].value
    if str(type(socset)) == "<class 'str'>":
        if s(socset) != '':
            contacts.append((id, 'instagram', s(socset)))
    socset = row[14].value
    if str(type(socset)) == "<class 'str'>":
        if s(socset) != '':
            contacts.append((id, 'twitter', s(socset)))
    socset = row[15].value
    if str(type(socset)) == "<class 'str'>":
        if s(socset) != '':
            contacts.append((id, 'vk', s(socset)))
    opisan = s(row[16].value)
    read_cursor.execute('SELECT * FROM two_gis WHERE two_gis.id = %s;', (id,))
    had_in_gis = read_cursor.fetchall()
    if len(had_in_gis) < 1:
        sql = 'INSERT INTO two_gis(id, id_fil, `name`, full_name, address, opisan) VALUES(%s,%s,%s,%s,%s,%s)'
        write_cursor.execute(sql, (id, id_fil, name, full_name, address, opisan))
    sql = 'INSERT INTO name_words(id_from_gis, name_word) VALUES(%s,%s)'
    write_cursor.executemany(sql, name_words)
    sql = 'INSERT INTO phones(id_from_gis, `type`, phone) VALUES(%s,%s,%s)'
    write_cursor.executemany(sql, phones_all)
    sql = 'INSERT INTO contacts(id_from_gis, `type`, contact) VALUES(%s,%s,%s)'
    write_cursor.executemany(sql, contacts)
    dbconn.commit()
    if i % 500 == 0:
        print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Записано в БД:', i)

dbconn.close()


