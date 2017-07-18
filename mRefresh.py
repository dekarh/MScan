# -*- coding: utf-8 -*-

#
# Предварительный сканер, сканирует только список
#


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from mysql.connector import MySQLConnection, Error
import datetime
from datetime import datetime
import time
import string
from libScan import wj, p, B, chk, authorize, to_spisok, set_filter, l, read_config

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')
scanconfig = read_config(section='scan')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(1) # Неявное ожидание - ждать ответа на каждый запрос до 1 сек
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

print('\n-------------------------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"), 'Начинаем всё заново'
                                                     '\n-------------------------------------\n')
authorize(driver, **webconfig)  # Авторизация
wj(driver)
to_spisok(driver)
wj(driver)
set_filter(driver, **scanconfig)
wj(driver)
g = 0
height = driver.get_window_size()['height']  # Высота окна
wj(driver)
read_cursor.execute('SELECT inn FROM pre_scan WHERE id >-1;')
rows = read_cursor.fetchall()
inns_from_bd = []
for row in rows:
    inns_from_bd.append(row[0])
print(datetime.strftime(datetime.now(), "%H:%M:%S"), ' ', len(inns_from_bd),
                                             ' ИНН в БД\n---------------------')
while g < 1000:
    try:
        gg = 0
        while gg < 100:
            ff = p(d=driver, f='c', **B['next'])
            wj(driver)
            ff.click()
            wj(driver)
            gg += 1
            if gg % 10 == 0:
                print(datetime.strftime(datetime.now(), "%H:%M:%S"), gg, 'перелистываний')
        print('---------------------\n', datetime.strftime( datetime.now(), "%H:%M:%S"),'100 страниц закэшировал')
        wj(driver)
        inns = p(d = driver, f = 'ps', **B['inn_spisA'])
        wj(driver)
        print('---------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"),len(inns) ,' ИНН в памяти\n---------------------')
        wj(driver)
        for i, inn in enumerate(inns):
            pass_string = False
            wj(driver)
            for inn_from_bd in inns_from_bd:
                if inn_from_bd == l(inn):
                    pass_string = True
            if pass_string:
                continue
            write_cursor.execute('INSERT INTO pre_scan(inn, inn2) VALUES( %s, %s )', (l(inn), l(inn)))
            dbconn.commit()
            inns_from_bd.append(l(inn))
            if len(inns_from_bd) % 100 == 0:
                print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Сканировано из списка: ', len(inns_from_bd))
        print('---------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"), len(inns_from_bd),
              ' ИНН в БД\n---------------------')

        #        f = p(d=driver, f='c', **B['next'])
#        wj(driver)
#        time.sleep(3)
#        f.click()
#        wj(driver)
#        print(datetime.strftime(datetime.now(), "%H:%M:%S"),'next внизу')
#        time.sleep(3)
    except Exception as ee:
        print(datetime.strftime(datetime.now(), "%H:%M:%S"),'Ошибка: ', ee, '\n\nПродолжаем ')
        continue

#    dbconn.close()
#    driver.close()
#    driver = webdriver.Chrome()  # Инициализация драйвера
#    driver.implicitly_wait(1)  # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
#    dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
#    read_cursor = dbconn.cursor()
#    write_cursor = dbconn.cursor()

dbconn.close()
driver.close()


