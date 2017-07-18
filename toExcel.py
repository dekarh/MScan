# -*- coding: utf-8 -*-

#
# Предварительный сканер, сканирует только список
#

from mysql.connector import MySQLConnection, Error
from datetime import datetime
import openpyxl
from openpyxl import Workbook

from libScan import read_config


wb = Workbook(write_only=True)
ws = wb.create_sheet('Лист1')

dbconfig = read_config(section='mysql')
exlconfig = read_config(section='excel')
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

print('\n\n', datetime.strftime(datetime.now(), "%H:%M:%S"), 'Начинаем экспорт из БД в excel')
read_cursor.execute('SELECT * FROM main WHERE inn >-1;')
rows = read_cursor.fetchall()

head = []                                           # Заголовок excel
for j, cell in enumerate(read_cursor.column_names):
    head.append(cell)
ws.append(head)

row = []
for i, row in enumerate(rows):
    rez_row = []
    for j, cell in enumerate(row):
        if cell == None:
            rez_cell = ''
        else:
            if head[j] == 'inn':
                if cell > 9999999999:
                    rez_cell = '{:0>12d}'.format(cell)
                else:
                    rez_cell = '{:0>10d}'.format(cell)
            elif head[j] == 'kpp':
                rez_cell = '{:0>9d}'.format(cell)
            elif head[j] == 'id' or head[j] == 'act_num':
                rez_cell = str(cell)
            elif head[j] == 'phone_1' or head[j] == 'phone_2' or head[j] == 'phone_3' or head[j] == 'phone_4' or \
                            head[j] == 'phone_5':
                rez_cell = '{:0>11d}'.format(cell)
            elif head[j] == 'okpo' or head[j] == 'oktmo':
                rez_cell = '{:0>8d}'.format(cell)
            elif head[j] == 'ogrn':
                rez_cell = '{:0>13d}'.format(cell)
            else:
                rez_cell = cell.strip().replace('\n',' ').replace('\r',' ').replace('"',"'")
            rez_row.append(rez_cell)
    ws.append(rez_row)
    if i % 100 == 0:
        print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Записано в excel:', i)

wb.save(**exlconfig)
dbconn.close()


