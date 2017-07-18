# -*- coding: utf-8 -*-

#
# Самый первый вариант сканера. Сканирует все и список и внутренности
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
from libScan import wj, p, B, chk, authorize, to_spisok, set_filter, read_config

# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')
scanconfig = read_config(section='scan')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(1) # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

try:
    authorize(driver, **webconfig)  # Авторизация
    #driver.get(**fillconfig)  # Открытие страницы где надо заполнять
    wj(driver)
    to_spisok(driver)
    wj(driver)
    set_filter(driver, **scanconfig)
    wj(driver)

    g = 0
    height = driver.get_window_size()['height'] # Высота окна
    while g < 1000:
        firms = p(d = driver, f = 'vv', **B['firms_trA'])
        read_cursor.execute('SELECT id, inn, kpp FROM main WHERE inn >-1;')
        rows = read_cursor.fetchall()
        for i, firm in enumerate(firms):
            pass_string = False
            wj(driver)
            for row in rows:
                if row[0] == int(firm):
                    pass_string = True
            if pass_string:
                continue
            firmu = p(d=driver, f='p', **B['data_id'], data_id=firm)
            if firmu.location['y'] < 105:
                wj(driver)
                f = p(d = driver, f = 'c', **B['prev'])
                wj(driver)
                time.sleep(2)
                f.click()
                wj(driver)
                print(datetime.strftime(datetime.now(), "%H:%M:%S"),'prev')
                time.sleep(2)
                break
            if firmu.location['y'] > (height - 79):
                f = p(d = driver, f = 'c', **B['next'])
                wj(driver)
                time.sleep(2)
                f.click()
                wj(driver)
                print(datetime.strftime(datetime.now(), "%H:%M:%S"),'next вверху')
                time.sleep(2)
                break
            wj(driver)
            if firmu.is_displayed():
                wj(driver)                                      # Если DOM изменилось доступ через data-id (он не меняется)
                firma = p(d = driver, f = 'c', **B['data_id'], data_id = firm)
    #            xc_dataid(driver,'data_id',str(firm.get_attribute('data-id')))
                wj(driver)
                data_id = firma.get_attribute('data-id')
                firma.click()
                wj(driver)
                time.sleep(4)
                inn = p(d = driver, f = 'p', **B['innA'])
                kpp = p(d = driver, f = 'p', **B['kppA'])
                firm_full_name = p(d = driver, f = 'p', **B['firm_full_nameA'])
                if firm_full_name == '':
                    firm_full_name = p(d = driver, f = 'p', **B['familyA']) + ' ' + p(d = driver, f = 'p', **B['nameA'])\
                                     + ' ' + p(d = driver, f = 'p', **B['surnameA'])
                gen_info = p(d = driver, f = 'p', **B['gen_infoA'])
                act_num = p(d = driver, f = 'p', **B['act_numA'])
                act_link = p(d = driver, f = 'c', **B['act_link']) # Страница видов деятельности
                wj(driver)
                act_link.click()
                wj(driver)
                time.sleep(4)
                act_by_count = p(d = driver, f = 'c', **B['act_by_count']) # Список по сколько на страницу
                wj(driver)
                act_by_count.click()
                act_num1000 = p(d = driver, f = 'c', **B['act_num1000']) # Выбираем по 1000 на страницу
                act_num1000.click()
                acts =  p(d = driver, f = 'ps', **B['acts'])
                act_list = ''
                for j, act in enumerate(acts):
                    wj(driver)
                    if act.is_displayed() and act.get_attribute('rowkey').find('.') > -1:
                        wj(driver)
                        act_list += act.get_attribute('rowkey') + ' '
                wj(driver)
                act_link.click()
                wj(driver)
                time.sleep(4)
                ch_title = p(d = driver, f = 'p', **B['ch_titleA'])
                ch_name = p(d = driver, f = 'p', **B['ch_nameA'])
                ch_surname = p(d = driver, f = 'p', **B['ch_surnameA'])
                if ch_name == '' and ch_surname == '':
                    ch_fio = gen_info
                    ch_title = 'Индивидуальный предприниматель'
                else:
                    ch_fio = ch_surname + ' ' + ch_name
                summ = p(d = driver, f = 'p', **B['summA'])
                cost = p(d = driver, f = 'p', **B['costA'])
                s_rats = p(d = driver, f = 'ps', **B['rat_sumA'])
                c_rats = p(d = driver, f = 'ps', **B['rat_costA'])
                while len(s_rats) < 2:
                    s_rats.append('')
                while len(c_rats) < 2:
                    c_rats.append('')
                havnt_in_about = []  # Что не нашли на странице "О компании"
                ph = p(d = driver, f = 'ps', **B['phonesA'])
                if ph[0] == '':
                    havnt_in_about.append('phones')
                ph_t = p(d = driver, f = 'ps', **B['phones_typA'])
                while len(ph) < 5:
                    ph.append(None)
                ph_n = []
                for j, tel in enumerate(ph):
                    tel = str(tel).strip()
                    if tel == '' or tel == None:
                        ph_n.append(None)
                    else:
                        tel = ''.join([char for char in tel if char in string.digits])
                        if len(tel) == 11:
                            if tel[0] in ['8', '9']:
                                ph_n.append(int('7' + tel[1:]))
                        elif len(tel) == 10:
                            ph_n.append(int('7' + tel))
                        else:
                            ph_n.append(None)
                while len(ph_t) < 5:
                    ph_t.append(None)
                warns = p(d = driver, f = 'ps', **B['warnA'])
                if warns[0] == '':
                    havnt_in_about.append('warnings')
                warn_datas = p(d = driver, f = 'ps', **B['warn_dataA'])
                warn = ''
                for j, w in enumerate(warns):
                    if j < len(warn_datas):
                        if warn_datas[j] != '':
                            warn += w + ' (' + warn_datas[j] + ') '
                        else:
                            warn += w + ' '
                    else:
                        warn += w + ' '
                emp_qty = p(d = driver, f = 'p', **B['emp_qtyA'])
                address = p(d = driver, f = 'p', **B['addressA'])
                region = address.split(',')[0]
                if address == '':
                    havnt_in_about.append('address')
                predstavs = p(d = driver, f = 'ps', **B['predstavA'])
                if predstavs[0] == '':
                    havnt_in_about.append('predstavs')
                predstav = ''
                for w in predstavs:
                    predstav += w.replace('\n',' - ') + ' '
                filials = p(d = driver, f = 'ps', **B['filialsA'])
                fils = ''
                if filials[0] != '':
                    for j, w in enumerate(filials):
                        if j % 2 == 0:
                            fils += w
                        else:
                            fils += ' (' + w + ') '
                else:
                    havnt_in_about.append('filials')

                if chk(d = driver, **B['contacts']):
                    contacts_page = p(d = driver, f = 'c', **B['contacts'])
                    wj(driver)
                    contacts_page.click()
                    for havnt in havnt_in_about:
                        if havnt == 'phones':
                            ph = p(d=driver, f='ps', **B['phonesA'])
                            ph_t = p(d=driver, f='ps', **B['phones_typA'])
                            while len(ph) < 5:
                                ph.append(None)
                            ph_n = []
                            for j, tel in enumerate(ph):
                                tel = str(tel).strip()
                                if tel == '' or tel == None:
                                    ph_n.append(None)
                                else:
                                    tel = ''.join([char for char in tel if char in string.digits])
                                    if len(tel) == 11:
                                        if tel[0] in ['8', '9']:
                                            ph_n.append(int('7' + tel[1:]))
                                    elif len(tel) == 10:
                                        ph_n.append(int('7' + tel))
                                    else:
                                        ph_n.append(None)
                            while len(ph_t) < 5:
                                ph_t.append(None)
                        elif havnt == 'warnings':
                            warns = p(d=driver, f='ps', **B['warnA'])
                            warn_datas = p(d=driver, f='ps', **B['warn_dataA'])
                            warn = ''
                            for j, w in enumerate(warns):
                                if j < len(warn_datas):
                                    if warn_datas[j] != '':
                                        warn += w + ' (' + warn_datas[j] + ') '
                                    else:
                                        warn += w + ' '
                                else:
                                    warn += w + ' '
                        elif havnt == 'address':
                            address = p(d=driver, f='p', **B['addressA'])
                            region = address.split(',')[0]
                        elif havnt == 'predstavs':
                            predstavs = p(d=driver, f='ps', **B['predstavA'])
                            predstav = ''
                            for w in predstavs:
                                predstav += w.replace('\n', ' - ') + ' '
                        elif havnt == 'filials':
                            filials = p(d=driver, f='ps', **B['filialsA'])
                            if filials[0] != '':
                                for j, w in enumerate(filials):
                                    if j % 2 == 0:
                                        fils += w
                                    else:
                                        fils += ' (' + w + ') '

                if chk(d = driver, **B['rekv']):
                    rekv_page = p(d = driver, f = 'c', **B['rekv'])
                    wj(driver)
                    rekv_page.click()
                ogrn = p(d=driver, f='p', **B['ogrnA'])
                okpo = p(d=driver, f='p', **B['okpoA'])
                oktmo = p(d=driver, f='p', **B['oktmoA'])
                reg_N_pfr = p(d=driver, f='p', **B['reg_N_pfrA'])
                reg_comp =  p(d=driver, f='p', **B['reg_comp']).replace('\n',' ')
                reg_gos =  p(d=driver, f='p', **B['reg_org']).replace('\n',' ')

                if chk(d = driver, **B['owners']):
                    own_page = p(d = driver, f = 'c', **B['owners'])
                    wj(driver)
                    own_page.click()
                u = []
                uchreds = p(d=driver, f='ps', **B['uchred'])
                for j in range(int(len(uchreds)/3)):
                    u.append('(' + uchreds[j*3 + 2] + '% / ' + uchreds[j*3 + 1] + ' руб.) '+ uchreds[j*3])
                while len(u) < 5:
                    u.append(None)
                d = []
                dochki = p(d=driver, f='ps', **B['dochki'])
                for j in range(int(len(dochki)/2)):
                    d.append('(ИНН ' + dochki[j*2 + 1] + ') '+ dochki[j*2])
                while len(d) < 5:
                    d.append(None)

                sql = 'INSERT INTO main(inn, kpp, firm_full_name, gen_info, act_num, act_list, ch_title, ' \
                      'ch_fio, summ, cost, sum_rat1, sum_rat2, cost_rat1, cost_rat2, t_phone_1, phone_1, t_phone_2,' \
                      ' phone_2, t_phone_3, phone_3, t_phone_4, phone_4, t_phone_5, phone_5, warn, emp_qty, address,' \
                      ' region, predstav, fils, ogrn, okpo, oktmo, reg_N_pfr, reg_comp, reg_gos, u1, u2, u3, u4, u5,' \
                      'd1, d2, d3, d4, d5) ' \
                      'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                      ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                write_cursor.execute(sql, (inn, kpp, firm_full_name, gen_info, act_num, act_list, ch_title,
                                           ch_fio, summ, cost, s_rats[0], s_rats[1], c_rats[0], c_rats[1], ph_t[0],
                                           ph_n[0], ph_t[1], ph_n[1], ph_t[2], ph_n[2], ph_t[3], ph_n[3], ph_t[4], ph_n[4],
                                           warn, emp_qty, address, region, predstav, fils, ogrn, okpo, oktmo, reg_N_pfr,
                                           reg_comp, reg_gos, u[0], u[1], u[2], u[3], u[4], d[0], d[1], d[2], d[3], d[4]))
                dbconn.commit()
                read_cursor.execute('SELECT count(*) FROM main WHERE inn >-1;')
                rows = read_cursor.fetchall()
                if int(rows[0][0]) % 100 == 0:
                    print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Спарсено', int(rows[0][0]))
                wj(driver)
                close = p(d = driver, f = 'c', **B['close'])
                wj(driver)
                close.click()
                wj(driver)
                time.sleep(4)
        if i == len(firms)-1:
            f = p(d=driver, f='c', **B['next'])
            wj(driver)
            time.sleep(2)
            f.click()
            wj(driver)
            print(datetime.strftime(datetime.now(), "%H:%M:%S"),'next внизу')
            time.sleep(2)

    dbconn.close()
    driver.close()

except Exception as ee:
    print(datetime.strftime(datetime.now(), "%H:%M:%S"),'Ошибка: ', ee, '\n перезагружаю')
    dbconn.close()
    driver.close()
    driver = webdriver.Chrome()  # Инициализация драйвера
    driver.implicitly_wait(1)  # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
    dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
    read_cursor = dbconn.cursor()
    write_cursor = dbconn.cursor()



