from mwindow import Ui_Form
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from PyQt5.QtCore import QDate, QDateTime, QSize, Qt
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

        webconfig = read_config(section='web')
        scanconfig = read_config(section='scan')

        self.drv = webdriver.Chrome()  # Инициализация драйвера
        self.drv.implicitly_wait(5)  # Неявное ожидание - ждать ответа на каждый запрос до 10 сек

#        authorize(self.drv, **webconfig)  # Авторизация
#        wj(self.drv)

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
        self.cbLink.setCurrentIndex(0)
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
        self.tableWidget.setColumnCount(5)             # Устанавливаем кол-во колонок
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
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(cell)))

        self.id_tek = self.id_all[0]
#        self.mamba_id_tek = self.mamba_id[self.id_tek]
#        self.msg_id_tek = self.msg_id[self.id_tek]
        # Устанавливаем заголовки таблицы
        self.tableWidget.setHorizontalHeaderLabels(["Вкл", "Имя", "Лет", "Сооб-", "щений"])

        # Устанавливаем выравнивание на заголовки
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(3).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(4).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableWidget.resizeColumnsToContents()
        return

    def click_tableWidget(self, index):
        self.updateHistory()
        self.id_tek = self.id_all[index.row()]
        self.cbLink.setCurrentIndex(self.t_link[self.id_tek])
        self.cbPeople.setCurrentIndex(self.t_people[self.id_tek])
        return None

    def click_cbLink(self):
        self.write_cursor.execute('UPDATE peoples SET t_link = %s WHERE id = %s',
                                  (self.cbLink.currentIndex(), self.id_tek))
        self.dbconn.commit()

    def click_cbPeople(self):
        self.write_cursor.execute('UPDATE peoples SET t_people = %s WHERE id = %s',
                                  (self.cbPeople.currentIndex(), self.id_tek))
        self.dbconn.commit()

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

    def click_pbRefresh(self):
        fillconfig = read_config(section='fill')
        self.drv.get(**fillconfig)  # Открытие страницы где поиск
        sql = 'INSERT INTO peoples(name_age, mamba_id, category, html, image) VALUES (%s,%s,%s,%s,%s)'
#        write_cursor.executemany()

#        logo = urllib.request.urlopen(
#            "http://www.marseille-tourisme.com/fileadmin/user_upload/plan_mars2013.jpg").read()

# "https://www.mamba.ru/mb1744035084?hit=35&sp=1".split("https://www.mamba.ru/")[1].split("?")[0]
# "https://www.mamba.ru/erdyk2008?hit=35&sp=1".split("https://www.mamba.ru/")[1].split("?")[0]

    def click_pbReLogin(self):
        q=0

    def click_pbScan(self):
        q=0

    def click_pbToAnketa(self):
        q=0

    def click_pbToMessage(self):
        q=0
