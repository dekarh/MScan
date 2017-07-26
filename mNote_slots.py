from mwindow import Ui_Form
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from PyQt5.QtCore import QDate, QDateTime, QSize, Qt, QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from os import popen
from libScan import read_config, LINK, PEOPLE, ONLINE, s, authorize, p, B, wj, wr
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MainWindowSlots(Ui_Form):   # Определяем функции, которые будем вызывать в слотах

    def setupUi(self, form):
        Ui_Form.setupUi(self,form)

        self.fillconfig = read_config(section='fill')
        self.webconfig = read_config(section='web')

        self.drv = webdriver.Chrome()  # Инициализация драйвера
        self.drv.implicitly_wait(5)  # Неявное ожидание - ждать ответа на каждый запрос до 5 сек

        dbconfig = read_config(section='mysql')
        self.dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
#        self.read_cursor = self.dbconn.cursor()
#        self.write_cursor = self.dbconn.cursor()

        self.id_all = []
        self.id_tek = 0
        self.mamba_id = {}
#        self.mamba_id_tek = ''
        self.msg_id = {}
#        self.msg_id_tek = ''
        self.t_people = {}
        self.t_link = {}
        self.html = {}
        self.foto = {}
        self.history = ''
        self.histories = {}
        self.stLinkFrom = 0
        self.cbLinkFrom.addItems(LINK)
        self.cbLinkFrom.setCurrentIndex(self.stLinkFrom)
        self.stLinkTo = 7
        self.cbLinkTo.addItems(LINK)
        self.cbLinkTo.setCurrentIndex(self.stLinkTo)
        self.stPeopleFrom = 7
        self.cbPeopleFrom.addItems(PEOPLE)
        self.cbPeopleFrom.setCurrentIndex(self.stPeopleFrom)
        self.stPeopleTo = 8
        self.cbPeopleTo.addItems(PEOPLE)
        self.cbPeopleTo.setCurrentIndex(self.stPeopleTo)
        self.stStatus = 2
        self.cbStatus.addItems(ONLINE)
        self.cbStatus.setCurrentIndex(self.stStatus)
        self.cbPeople.addItems(PEOPLE)
        self.cbPeople.setCurrentIndex(0)
        self.cbLink.addItems(LINK)
        self.cbLink.setCurrentIndex(6)
        self.setup_tableWidget()
        return

    def click_pbPeopleFilter(self):  # Ненужная кнопка, все фильтруется по смене любого combobox'а
        self.setup_tableWidget()

    def setup_tableWidget(self):
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)        # Кол-во строк из таблицы
        read_cursor = self.dbconn.cursor()
        if self.stStatus == 2:
            read_cursor.execute('SELECT IF(status=0,"OFFline","ONline"), her_name, age, msg, unread_msg, id, msg_id,'
                                ' mamba_id, t_people, t_link, html, foto, history FROM peoples WHERE t_link >= %s'
                                ' AND t_link <= %s AND t_people >= %s AND t_people <= %s AND html IS NOT NULL '
                                'ORDER BY age DESC;',
                                (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo))
        else:
            read_cursor.execute('SELECT IF(status=0,"OFFline","ONline"), her_name, age, msg, unread_msg, id, msg_id, '
                                'mamba_id, t_people, t_link, html, foto, history FROM peoples WHERE t_link >= %s '
                                'AND t_link <= %s AND t_people >= %s  AND t_people <= %s AND status = %s '
                                'AND html IS NOT NULL ORDER BY age DESC;',
                                (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo, self.stStatus))

        rows = read_cursor.fetchall()
        self.tableWidget.setColumnCount(3)             # Устанавливаем кол-во колонок
        self.tableWidget.setRowCount(len(rows))        # Кол-во строк из таблицы
        self.id_all = []
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if j == len(row) - 8:
                    self.id_all.append(int(cell))
                    self.id_tek = int(cell)
                elif j == len(row) - 1:
                    self.histories[self.id_tek] = cell
                elif j == len(row) - 2:
                    self.foto[self.id_tek] = cell
                elif j == len(row) - 3:
                    self.html[self.id_tek] = cell
                elif j == len(row) - 4:
                    self.t_link[self.id_tek] = cell
                elif j == len(row) - 5:
                    self.t_people[self.id_tek] = cell
                elif j == len(row) - 6:
                    self.mamba_id[self.id_tek] = cell
                elif j == len(row) - 7:
                    self.msg_id[self.id_tek] = cell
                elif j == len(row) - 9:
                    q = 0                                           # сообщения не показывает, с...
                elif j == len(row) - 10:
                    q = 0
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(cell)))

        self.id_tek = self.id_all[0]
#        self.mamba_id_tek = self.mamba_id[self.id_tek]
#        self.msg_id_tek = self.msg_id[self.id_tek]
        # Устанавливаем заголовки таблицы
        self.tableWidget.setHorizontalHeaderLabels(["Статус", "Имя", "Возраст"])

        # Устанавливаем выравнивание на заголовки
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableWidget.resizeColumnsToContents()
        return

    def click_tableWidget(self, index):
        self.updateHistory()
        self.id_tek = self.id_all[index.row()]
        self.textEdit.setText(self.histories[self.id_tek])
        self.cbLink.setCurrentIndex(self.t_link[self.id_tek])
        self.cbPeople.setCurrentIndex(self.t_people[self.id_tek])
        pixmap = QPixmap()
        pixmap.loadFromData(self.foto[self.id_tek],'JPG')
        self.label_3.setPixmap(pixmap)
        self.anketa_html.setHtml(self.html[self.id_tek])
        return None

    def click_cbLink(self):
        write_cursor = self.dbconn.cursor()
        write_cursor.execute('UPDATE peoples SET t_link = %s WHERE id = %s',
                                  (self.cbLink.currentIndex(), self.id_tek))
        self.dbconn.commit()
        self.t_link[self.id_tek] = self.cbLink.currentIndex()
        if len(s(self.histories[self.id_tek])) > 0:
            self.textEdit.setText(s(self.histories[self.id_tek]) + '\n' + datetime.now().strftime("%d.%m.%y") +
                              ' этап-> ' +  s(self.cbLink.currentText()))
        else:
            self.textEdit.setText(s(self.histories[self.id_tek]) + datetime.now().strftime("%d.%m.%y") +
                              ' этап-> ' +  s(self.cbLink.currentText()))
        self.updateHistory()


    def click_cbPeople(self):
        write_cursor = self.dbconn.cursor()
        write_cursor.execute('UPDATE peoples SET t_people = %s WHERE id = %s',
                                  (self.cbPeople.currentIndex(), self.id_tek))
        self.dbconn.commit()
        self.t_people[self.id_tek] = self.cbPeople.currentIndex()
        if len(s(self.histories[self.id_tek])) > 0:
            self.textEdit.setText(s(self.histories[self.id_tek]) + '\n' + datetime.now().strftime("%d.%m.%y") +
                              ' чел.-> ' +  self.cbPeople.currentText())
        else:
            self.textEdit.setText(s(self.histories[self.id_tek]) + datetime.now().strftime("%d.%m.%y") +
                              ' чел.-> ' +  self.cbPeople.currentText())
        self.updateHistory()

    def click_cbLinkFrom(self):
        self.stLinkFrom = self.cbLinkFrom.currentIndex()
        self.setup_tableWidget()

    def click_cbLinkTo(self):
        self.stLinkTo = self.cbLinkTo.currentIndex()
        self.setup_tableWidget()

    def click_cbStatus(self):
        self.stStatus = self.cbStatus.currentIndex()
        self.setup_tableWidget()

    def click_cbPeopleFrom(self):
        self.stPeopleFrom = self.cbPeopleFrom.currentIndex()
        self.setup_tableWidget()

    def click_cbPeopleTo(self):
        self.stPeopleTo = self.cbPeopleTo.currentIndex()
        self.setup_tableWidget()

    def updateHistory(self):
        current = self.textEdit.toPlainText()
        if self.histories[self.id_tek] == None:
            past = ''
        else:
            past = self.histories[self.id_tek]
        if current != past:
            write_cursor = self.dbconn.cursor()
            write_cursor.execute('UPDATE peoples SET history = %s WHERE id = %s', (current, self.id_tek))
            self.dbconn.commit()
            self.histories[self.id_tek] = current

    def convert_mamba_id(self, href):
        a = "".join([k.strip() for k in href]).strip()
        m_id = a[21:].split("?")[0]
        print(a, a[21:], m_id)
        return m_id

    def convert_msg_id(self, m_id):
        if m_id[:2] == 'mb':
            return m_id[2:]
        else:
            return None

    def click_pbScan(self):
        self.drv.get(**self.fillconfig)  # Открытие страницы где поиск

        page = 1
        standart = len(p(d=self.drv, f='ps', **B['tiles']))
        while len(p(d=self.drv, f='ps', **B['tiles'])) == standart:
            if page > 1:
                wj(self.drv)
                page_link = self.drv.find_element_by_xpath('//DIV[@class="pager wrap"]//LI[text()="' + str(page) + '"]')
                wj(self.drv)
                page_link.click()
                wj(self.drv)
            tiles = []
            tiles = p(d=self.drv, f='ps', **B['tiles'])
            hrefs = []
            hrefs = p(d=self.drv, f='ps', **B['tiles-href'])
            for i, mamba_href in enumerate(hrefs):
                mamba_id = self.convert_mamba_id(mamba_href)
                row_ch = []
                read_cursor = self.dbconn.cursor()
                read_cursor.execute('SELECT mamba_id, html FROM peoples WHERE mamba_id = %s', (mamba_id,))
                row_ch = read_cursor.fetchall()
                refresh_html = False  # анкета сохранена в базе?
                if len(row_ch) > 0:
                    if row_ch[0][1] == None:
                        refresh_html = True
                    elif len(row_ch[0][1]) < 10:
                        refresh_html = True
                else:
                    refresh_html = True
                if len(row_ch) < 1:  # такой записи нет в базе
                    continue
                elif refresh_html:  # запись есть, а анкеты нет
                    tiles[i].click()
                    wj(self.drv)
                    html_msg = p(d=self.drv, f='p', **B['anketa-msg'])
                    html_favour = p(d=self.drv, f='p', **B['anketa-favour'])
                    html_abouts = p(d=self.drv, f='ps', **B['anketa-about'])
                    html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/' \
                           'strict.dtd"><html><head></head><body><p>' + html_msg + '</p><p>'
                    html += html_favour.replace('\n',' | ') + '</p>'
                    if len(html_abouts) > 0:
                        for html_into in html_abouts:
                            html += html_into
                    html = html.replace('\n',' ').replace('\t',' ').replace('  ',' ').replace('  ',' ')
                    html = html.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
                    html = html.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
                    html += '</body></html>'
                    read_cursor = self.dbconn.cursor()
                    read_cursor.execute('SELECT msg_id FROM peoples WHERE mamba_id = %s', (mamba_id,))
                    row_msg = read_cursor.fetchall()
                    if len(row_msg) > 0:
                        if row_msg[0][0] == None:
                            sql = 'UPDATE peoples SET msg_id = %s WHERE mamba_id = %s'
                            write_cursor = self.dbconn.cursor()
                            aa = p(d=self.drv, f='p', **B['anketa-btn'])
                            ab = aa.split('uid=')[1]
                            write_cursor.execute(sql, (ab, mamba_id))
                            self.dbconn.commit()
                    wj(self.drv)
                    wr()
                    back = p(d=self.drv, f='c', **B['back-find'])
                    wj(self.drv)
                    sql = 'UPDATE peoples SET html = %s WHERE mamba_id = %s'
                    write_cursor = self.dbconn.cursor()
                    write_cursor.execute(sql, (html, mamba_id))
                    self.dbconn.commit()
                    back.click()
                    wj(self.drv)
                    break
                else:                                               # есть и запись и анкета
                    continue
            page += 1
            q = 0
        q = 0

    def click_pbReLogin(self):
        self.drv.quit()
        self.drv = webdriver.Chrome()  # Инициализация драйвера
        self.drv.implicitly_wait(5)  # Неявное ожидание - ждать ответа на каждый запрос до 5 сек
        authorize(self.drv, **self.webconfig)  # Авторизация
        wj(self.drv)


    def click_pbRefresh(self):                                  # Обновление статусов
        """
        self.drv.get(**self.fillconfig)  # Открытие страницы где поиск

        page = 1
        standart = len(p(d=self.drv, f='ps', **B['tiles']))
        while len(p(d=self.drv, f='ps', **B['tiles'])) == standart:
            outs = []
            statuses = []
            status_and_html = []
            if page > 1:
                page_link = self.drv.find_element_by_xpath('//DIV[@class="pager wrap"]//LI[text()="' + str(page) + '"]')
                page_link.click()
            tiles = []
            tiles = p(d=self.drv, f='ps', **B['tiles'])
            names = []
            names = p(d=self.drv, f='ps', **B['tiles-name'])
            hrefs = []
            hrefs = p(d=self.drv, f='ps', **B['tiles-href'])
            fotos_hrefs = []
            fotos_hrefs = p(d=self.drv, f='ps', **B['tiles-img'])
            hrefs_onln = []
            hrefs_onln = p(d=self.drv, f='ps', **B['tiles-onln'])
            for i, mamba_href in enumerate(hrefs):
                mamba_id = self.convert_mamba_id(mamba_href)
                row_ch = []
                read_cursor = self.dbconn.cursor()
                read_cursor.execute('SELECT mamba_id, html FROM peoples WHERE mamba_id = %s',(mamba_id,))
                row_ch = read_cursor.fetchall()
                refresh_html = False                                # анкета сохранена в базе?
                if len(row_ch) > 0:
                    if row_ch[0][1] == None:
                        refresh_html = True
                    elif len(row_ch[0][1]) < 10:
                        refresh_html = True
                else:
                    refresh_html = True
                if len(row_ch) < 1:                                 # такой записи нет в базе
                    out = tuple()
                    age = ('0',)
                    if len(names[i].split(',')) > 1:
                        age = (names[i].split(',')[1].strip(), )
                    out += (mamba_id, ) + (self.convert_msg_id(mamba_id), ) + (names[i].split(',')[0].strip(), ) + age
                    status = 0
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                    foto = urllib.request.urlopen(fotos_hrefs[i]).read()

                    if refresh_html:
                        q=0
                    else:
                        html = row_ch[0][1]
                    out += (status, ) + (foto, ) + (html,)
                    outs.append(out)
                elif refresh_html:                                  # запись есть, а анкеты нет
                    status = 0
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                    tiles[i].click()
                    wj(self.drv)
                    html = p(d=self.drv, f='p', **B['anketa-html'])
                    wj(self.drv)
                    wr()
                    back = p(d=self.drv, f='c', **B['back-find'])
                    wj(self.drv)
                    back.click()
                    status_and_html.append((status, html, mamba_id))

                else:                                               # есть и запись и анкета
                    status = 0
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                    statuses.append((status, mamba_id))
            if len(status_and_html) > 0:
                sql = 'UPDATE peoples SET status = %s, html = %s WHERE mamba_id = %s'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, status_and_html)
                self.dbconn.commit()
            if len(outs) > 0:
                sql = 'INSERT INTO peoples(mamba_id, msg_id, her_name, age, status, foto, html) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, outs)
                self.dbconn.commit()
            if len(statuses) > 0:
                sql = 'UPDATE peoples SET status = %s WHERE mamba_id = %s'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, statuses)
                self.dbconn.commit()
            page += 1
            q=0
        q = 0
        """

        sql = 'UPDATE peoples SET status = %s WHERE id > 0'     # Сначала всех в оффлайн
        write_cursor = self.dbconn.cursor()
        write_cursor.execute(sql, (0,))
        self.dbconn.commit()

        self.drv.get(**self.fillconfig)  # Открытие страницы где поиск

        page = 1
        standart = len(p(d=self.drv, f='ps', **B['tiles']))
        while len(p(d=self.drv, f='ps', **B['tiles'])) == standart:
            outs = []
            statuses = []
            if page > 1:
                page_link = self.drv.find_element_by_xpath('//DIV[@class="pager wrap"]//LI[text()="' + str(page) + '"]')
                page_link.click()
            names = []
            names = p(d=self.drv, f='ps', **B['tiles-name'])
            hrefs = []
            hrefs = p(d=self.drv, f='ps', **B['tiles-href'])
            fotos_hrefs = []
            fotos_hrefs = p(d=self.drv, f='ps', **B['tiles-img'])
            hrefs_onln = []
            hrefs_onln = p(d=self.drv, f='ps', **B['tiles-onln'])
            for i, mamba_href in enumerate(hrefs):
                mamba_id = self.convert_mamba_id(mamba_href)
                row_ch = []
                read_cursor = self.dbconn.cursor()
                read_cursor.execute('SELECT mamba_id FROM peoples WHERE mamba_id = %s',(mamba_id,))
                row_ch = read_cursor.fetchall()
                if len(row_ch) < 1:
                    out = tuple()
                    age = ('0',)
                    if len(names[i].split(',')) > 1:
                        age = (names[i].split(',')[1].strip(), )
                    out += (mamba_id, ) + (self.convert_msg_id(mamba_id), ) + (names[i].split(',')[0].strip(), ) + age
                    status = 0
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                    foto = urllib.request.urlopen(fotos_hrefs[i]).read()
                    out += (status, ) + (foto, )
                    outs.append(out)
                else:
                    status = 0
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                    statuses.append((status, mamba_id))
            if len(outs) > 0:
                sql = 'INSERT INTO peoples(mamba_id, msg_id, her_name, age, status, foto) VALUES (%s,%s,%s,%s,%s,%s)'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, outs)
                self.dbconn.commit()
            if len(statuses) > 0:
                sql = 'UPDATE peoples SET status = %s WHERE mamba_id = %s'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, statuses)
                self.dbconn.commit()
            page += 1
            q=0
        q = 0


    def click_pbToAnketa(self):
        q=0

    def click_pbToMessage(self):
        q=0
