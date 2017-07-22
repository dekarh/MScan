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

        authorize(self.drv, **webconfig)  # Авторизация
        wj(self.drv)

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
        self.history = {}
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
        self.stPeople = 0
        self.cbPeople.addItems(PEOPLE)
        self.cbPeople.setCurrentIndex(self.stPeople)
        self.stLink = 0
        self.cbLink.addItems(LINK)
        self.cbLink.setCurrentIndex(self.stLink)
        self.setup_tableWidget()
        return

    def click_pbPeopleFilter(self):  # Ненужная кнопка, все фильтруется по смене любого combobox'а
        self.setup_tableWidget()

    def setup_tableWidget(self):
        if self.stStatus == 2:
            self.read_cursor.execute('SELECT IF(status=0,"OFF,"ONL"), her_name, age, msg, unread_msg, id, msg_id, mamba_id,'
                                     ' t_people, t_link, html, foto, history FROM peoples '
                                     'WHERE t_link >= %s AND t_link <= %s AND t_people >= %s AND t_people <= %s;',
                                     (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo))
        else:
            self.read_cursor.execute('SELECT IF(status=0,"OFF,"ONL"), her_name, age, msg, unread_msg, id, msg_id, mamba_id,'
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
                    self.history[self.id_tek] = cell
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
# "https://www.mamba.ru/mb1744035084?hit=35&sp=1".split("https://www.mamba.ru/")[1].split("?")[0]
# "https://www.mamba.ru/erdyk2008?hit=35&sp=1".split("https://www.mamba.ru/")[1].split("?")[0]
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
        self.innFIO = self.tableFIOmain.model().index(index.row(), 0).data()
        self.curFIO = self.tableFIOmain.model().index(index.row(), 1).data()
        self.updateHistory()
        self.id_tek = self.id_all[index.row()]
        self.mamba_id_tek = self.mamba_id[self.id_tek]
        self.msg_id_tek = self.msg_id[self.id_tek]
        self.comboBoxTek.setCurrentIndex(int(self.steps[int(self.innFIO)]))
        return None

    def click_comboBoxTek(self):
        self.write_cursor.execute('UPDATE fio SET step = %s WHERE inn_fio = %s',
                                  (self.comboBoxTek.currentIndex(), self.innFIO))
        self.dbconn.commit()
        self.steps[int(self.innFIO)] = self.comboBoxTek.currentIndex()
        q=0

    def click_comboBoxPoor(self):
        self.step_poor = self.comboBoxPoor.currentIndex()
        self.setup_tableFIOmain()

    def click_comboBoxGood(self):
        self.step_good = self.comboBoxGood.currentIndex()
        self.setup_tableFIOmain()

    def updateHistory(self):
        current = self.textHistory.toPlainText()
        if self.histories[int(self.last_innFIO)] == None:
            past = ''
        else:
            past = self.histories[int(self.last_innFIO)]
        if current != past:
            self.write_cursor.execute('UPDATE fio SET history = %s WHERE inn_fio = %s', (current, self.last_innFIO))
            self.dbconn.commit()
            self.histories[int(self.last_innFIO)] = current
        self.last_innFIO = self.innFIO
        self.textHistory.setText(self.histories[int(self.innFIO)])

    def click_pbRefresh(self):
        fillconfig = read_config(section='fill')
        self.drv.get(**fillconfig)  # Открытие страницы где поиск
        sql = 'INSERT INTO peoples(name_age, mamba_id, category, html, image) VALUES (%s,%s,%s,%s,%s)'
#        write_cursor.executemany()

        logo = urllib.request.urlopen(
            "http://www.marseille-tourisme.com/fileadmin/user_upload/plan_mars2013.jpg").read()







    def setup_tableFirms(self):
        self.read_cursor.execute("SELECT IF(LEFT(UCASE(m.firm_full_name),8) = 'ОБЩЕСТВО', "
                "REPLACE(SUBSTR(UCASE(m.firm_full_name),42),'\"',' '), UCASE(m.firm_full_name)) AS `OOO`,"
                " m.predstav, m.address, m.phone_1, m.phone_2, m.phone_3, m.phone_4, m.phone_5, FORMAT(q.summ,0),"
                "FORMAT(q.cost,0), m.inn, m.act_list, m.description "
                "FROM main2fio AS q LEFT JOIN main AS m ON m.inn = q.main_inn WHERE q.fio_inn_fio = %s", (self.innFIO,))
        rows = self.read_cursor.fetchall()
        self.tableFirms.setColumnCount(12)               # Устанавливаем кол-во колонок
        self.tableFirms.setRowCount(len(rows))           # Кол-во строк из таблицы
        self.okwed_lists = []
        self.tableFirms_inns = []
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if j == len(row) - 3:
                    self.tableFirms_inns.append(cell)
                    if cell == None:
                        self.tableFirms.setItem(i, j, QTableWidgetItem(''))
                    else:
                        self.tableFirms.setItem(i, j, QTableWidgetItem(str(cell)))
                if j == len(row) - 2:
                    self.okwed_lists.append(str(cell))
                elif j == len(row) - 1:
                    self.descriptions[self.tableFirms_inns[i]] = cell
                else:
                    if cell == None:
                        self.tableFirms.setItem(i, j, QTableWidgetItem(''))
                    else:
                        self.tableFirms.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableFirms.setHorizontalHeaderLabels(['ООО', 'Представитель', 'Адрес', '', '', '',
                                                     '', '', 'Сумма', 'Стоимость', 'ИНН'])

        # Устанавливаем выравнивание на заголовки
        for i in range(8):
            self.tableFirms.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFirms.resizeColumnsToContents()

        return

    def updateDescription(self):
        current = self.textDescription.toPlainText()
        if self.descriptions[int(self.last_inn)] == None:
            past = ''
        else:
            past = self.descriptions[int(self.last_inn)]
        if current != past:
            self.write_cursor.execute('UPDATE main SET description = %s WHERE inn = %s', (current, self.last_inn))
            self.dbconn.commit()
            self.descriptions[int(self.last_inn)] = current
        self.last_inn = self.inn
        self.textDescription.setText(self.descriptions[int(self.inn)])


    def click_tableFirms(self, index=None):
        if index == None:
            index = self.tableFirms.model().index(0, 0)
        self.curOOO = self.tableFirms.model().index(index.row(), 0).data()
        self.setup_tableOKWED(self.okwed_lists[index.row()])
        self.setup_table2GIS(self.tableFirms_inns[index.row()])
        self.click_table2GIS()
        self.setup_tableFIO(self.tableFirms_inns[index.row()])
        self.updateHistory()
        self.inn = self.tableFirms_inns[index.row()]
        self.updateDescription()
        g = 0
#        google-chrome "duckduckgo.com/?q=+телефон+ИВАНЧУГСКИЙ+КОНСЕРВНЫЙ+ЗАВОД"

    def setup_tableOKWED(self, okwed_list):
        okwed_list_with_or = ''
        okwed_list_t = ()
        for i, okwed in enumerate(okwed_list.strip().split(' ')):
            okwed_list_t += (okwed, )
            if i == len(okwed_list.strip().split()) - 1:
                okwed_list_with_or += ' okwed = %s'
            else:
                okwed_list_with_or += ' okwed = %s OR '
        self.read_cursor.execute("SELECT  okwed, about FROM okwed WHERE" + okwed_list_with_or, okwed_list_t)
        rows = self.read_cursor.fetchall()
        self.tableOKWED.setColumnCount(2)  # Устанавливаем кол-во колонок
        self.tableOKWED.setRowCount(len(rows))  # Кол-во строк из таблицы
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.tableOKWED.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableOKWED.setHorizontalHeaderLabels(['Код', 'Значение'])

        # Устанавливаем выравнивание на заголовки
        for i in range(2):
            self.tableOKWED.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableOKWED.resizeColumnsToContents()

        return

    def setup_table2GIS(self, inn):
        self.tableFirm2gis.setColumnCount(0)
        self.tableFirm2gis.setRowCount(0)
        self.read_cursor.execute("SELECT g.word, t.full_name, t.id, t.address, t.opisan FROM main2gis AS g "
                                 "LEFT JOIN two_gis AS t ON g.id_from_gis=t.id "
                                 "LEFT JOIN main AS m ON g.main_inn=m.inn WHERE m.inn = %s", (inn,))
        rows = self.read_cursor.fetchall()
        self.tableFirm2gis.setColumnCount(2)               # Устанавливаем кол-во колонок
        self.tableFirm2gis.setRowCount(len(rows))          # Кол-во строк из таблицы
        self.GISids = []
        self.GISabouts = []
        self.GISaddreses = []
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if j == len(row) - 3:
                    self.GISids.append(str(cell))
                if j == len(row) - 2:
                    self.GISaddreses.append(str(cell))
                elif j == len(row) - 1:
                    self.GISabouts.append(str(cell))
                else:
                    self.tableFirm2gis.setItem(i, j, QTableWidgetItem(str(cell)))


        # Устанавливаем заголовки таблицы
        self.tableFirm2gis.setHorizontalHeaderLabels(['Слово', 'Компания'])

        # Устанавливаем выравнивание на заголовки
        for i in range(2):
            self.tableFirm2gis.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFirm2gis.resizeColumnsToContents()

        return

    def click_table2GIS(self, index=None):
        if index == None:
            index = self.tableFirm2gis.model().index(0, 0)
        self.setup_tableContacts2gis(index.row())
#        self.updateHistory()
#        self.updateDescription()


    def setup_tableContacts2gis(self, row_number):
        self.label_desc.clear()
        self.tableContacts2gis.setColumnCount(0)
        self.tableContacts2gis.setRowCount(0)
        if len(self.GISids) > 0:
            self.read_cursor.execute('SELECT `type`, contact FROM contacts WHERE id_from_gis = %s',
                                     (int(self.GISids[row_number]),))
            rows = self.read_cursor.fetchall()
            self.tableContacts2gis.setColumnCount(2)             # Устанавливаем кол-во колонок
            self.tableContacts2gis.setRowCount(len(rows))        # Кол-во строк из таблицы
            for i, row in enumerate(rows):
                for j, cell in enumerate(row):
                    self.tableContacts2gis.setItem(i, j, QTableWidgetItem(str(cell)))

            # Устанавливаем заголовки таблицы
            self.tableContacts2gis.setHorizontalHeaderLabels(["Тип", "Контакт"])

            # Устанавливаем выравнивание на заголовки
            self.tableContacts2gis.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
            self.tableContacts2gis.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)

            # делаем ресайз колонок по содержимому
            self.tableContacts2gis.resizeColumnsToContents()
            next_string = False
            addr = ''
            for i, char in enumerate(self.GISaddreses[row_number]):
                if i % 40 == 0 and i != 0:
                    next_string = True
                if next_string and char == ' ':
                    addr += char + '<br />'
                    next_string = False
                else:
                    addr += char
            self.label_desc.setText('<b>' + addr + '</b> <br />' + self.GISabouts[row_number])
        return

    def setup_tableFIO(self, inn):
        self.tableFIO.setColumnCount(0)
        self.tableFIO.setRowCount(0)
        self.read_cursor.execute('SELECT f.inn_fio, CONCAT_WS(" ", f.`name`, f.surname, f.family), '
                                 'FORMAT(q.summ,0), '
                                 'FORMAT((select sum(q.summ) FROM main2fio AS q WHERE f.inn_fio = q.fio_inn_fio),0),'
                                 'FORMAT(q.cost,0), '                                 
                                 'FORMAT((select sum(q.cost) FROM main2fio AS q WHERE f.inn_fio = q.fio_inn_fio),0) '
                                 'FROM main2fio AS q '
                                 'LEFT JOIN fio AS f ON q.fio_inn_fio = f.inn_fio WHERE q.main_inn = %s '
                                 'ORDER BY family', (inn,))
        rows = self.read_cursor.fetchall()
        self.tableFIO.setColumnCount(6)             # Устанавливаем кол-во колонок
        self.tableFIO.setRowCount(len(rows))        # Кол-во строк из таблицы
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.tableFIO.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableFIO.setHorizontalHeaderLabels(["ИНН", "Имя Отчество Фамилия","Прибыль","ИТОГО","Стоимость","ИТОГО"])

        # Устанавливаем выравнивание на заголовки
        self.tableFIO.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.tableFIO.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFIO.resizeColumnsToContents()

        return



