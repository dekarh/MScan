from mwindow import Ui_Form
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from PyQt5.QtCore import QDate, QDateTime, QSize, Qt, QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from os import popen
from libScan import read_config, LINK, PEOPLE, ONLINE, l, authorize, p, B, wj
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
        self.read_cursor = self.dbconn.cursor()
        self.write_cursor = self.dbconn.cursor()

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
        self.stPeopleFrom = 6
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
        if self.stStatus == 2:
            self.read_cursor.execute('SELECT IF(status=0,"OFF","ONL"), her_name, age, msg, unread_msg, id, msg_id, mamba_id,'
                                     ' t_people, t_link, html, foto, history FROM peoples '
                                     'WHERE t_link >= %s AND t_link <= %s AND t_people >= %s AND t_people <= %s;',
                                     (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo))
        else:
            self.read_cursor.execute('SELECT IF(status=0,"OFF","ONL"), her_name, age, msg, unread_msg, id, msg_id, mamba_id,'
                                     ' t_people, t_link, html, foto, history FROM peoples '
                                     'WHERE t_link >= %s AND t_link <= %s AND t_people >= %s  AND t_people <= %s '
                                     'AND status = %s;',
                                     (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo, self.stStatus))

        rows = self.read_cursor.fetchall()
        self.tableWidget.setColumnCount(3)             # Устанавливаем кол-во колонок
        self.tableWidget.setRowCount(len(rows))        # Кол-во строк из таблицы
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
                    q = 0
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
        return None

    def click_cbLink(self):
        self.write_cursor.execute('UPDATE peoples SET t_link = %s WHERE id = %s',
                                  (self.cbLink.currentIndex(), self.id_tek))
        self.dbconn.commit()
        if len(self.histories[self.id_tek]) > 0:
            self.textEdit.setText(self.histories[self.id_tek] + '\n' + datetime.now().strftime("%d:%m:%y") +
                              ' этап-> ' +  self.cbLink.currentText())
        else:
            self.textEdit.setText(self.histories[self.id_tek] + datetime.now().strftime("%d:%m:%y") +
                              ' этап-> ' +  self.cbLink.currentText())
        self.updateHistory()


    def click_cbPeople(self):
        self.write_cursor.execute('UPDATE peoples SET t_people = %s WHERE id = %s',
                                  (self.cbPeople.currentIndex(), self.id_tek))
        self.dbconn.commit()
        if len(self.histories[self.id_tek]) > 0:
            self.textEdit.setText(self.histories[self.id_tek] + '\n' + datetime.now().strftime("%d:%m:%y") +
                              ' чел.-> ' +  self.cbPeople.currentText())
        else:
            self.textEdit.setText(self.histories[self.id_tek] + datetime.now().strftime("%d:%m:%y") +
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

    def updateHistory(self):    # Проверить нужно ли last_id_tek
        current = self.textEdit.toPlainText()
        if self.histories[self.id_tek] == None:
            past = ''
        else:
            past = self.histories[self.id_tek]
        if current != past:
            self.write_cursor.execute('UPDATE peoples SET history = %s WHERE id = %s', (current, self.id_tek))
            self.dbconn.commit()
            self.histories[self.id_tek] = current
#        self.last_innFIO = self.innFIO
#        self.textHistory.setText(self.histories[int(self.innFIO)])

    def convert_mamba_id(self, href):
        a = "".join([i.strip() for i in href])
        m_id = a.strip().split("https://www.mamba.ru/")[1].split("?")[0]
        return m_id

    def convert_msg_id(self, m_id):
        if m_id[:2] == 'mb':
            return m_id[2:]
        else:
            return None

    def click_pbRefresh(self):
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
                self.read_cursor.execute('SELECT mamba_id FROM peoples WHERE mamba_id = %s',(mamba_id,))
                row_ch = self.read_cursor.fetchall()
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
                self.write_cursor.executemany(sql, outs)
                self.dbconn.commit()
            if len(statuses) > 0:
                sql = 'UPDATE peoples SET status = %s WHERE mamba_id = %s'
                self.write_cursor.executemany(sql, statuses)
                self.dbconn.commit()
            page += 1
            q=0
        q = 0

    def click_pbReLogin(self):
        self.drv.quit()
        self.drv = webdriver.Chrome()  # Инициализация драйвера
        self.drv.implicitly_wait(5)  # Неявное ожидание - ждать ответа на каждый запрос до 5 сек

        authorize(self.drv, **self.webconfig)  # Авторизация
        wj(self.drv)


    def click_pbScan(self):
        q=0

    def click_pbToAnketa(self):
        q=0

    def click_pbToMessage(self):
        q=0
