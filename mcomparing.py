# -*- coding: utf-8 -*-
__author__ = 'Denis'

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate

from comparing_slots import MainWindowSlots



class MainWindow(MainWindowSlots):

    # При инициализации класса нам необходимо выполнить некоторые операции
    def __init__(self, form):
        # Сконфигурировать интерфейс методом из базового класса Ui_Form
        self.setupUi(form)
        # Подключить созданные нами слоты к виджетам
        self.connect_slots()

    # Подключаем слоты к виджетам (для каждого действия, которое надо обработать - свой слот)
    def connect_slots(self):
        self.tableFIOmain.pressed.connect(self.click_tableFIOmain)
        self.tableFIOmain.clicked.connect(self.click_tableFIOmain)
        self.tableFirms.clicked.connect(self.click_tableFirms)
        self.tableFirm2gis.clicked.connect(self.click_table2GIS)
        self.comboBoxTek.activated[str].connect(self.click_comboBoxTek)
        self.comboBoxGood.activated[str].connect(self.click_comboBoxGood)
        self.comboBoxPoor.activated[str].connect(self.click_comboBoxPoor)
        self.pushButtonFind.clicked.connect(self.buttonFindClicked)
        self.pushButtonFilter.clicked.connect(self.buttonFilterClicked)
        self.lineEdit.textChanged[str].connect(self.onLEChanged)
#        self.pushButton.clicked.connect(sys(exit(app.exec())))
        return None

if __name__ == '__main__':
    # Создаём экземпляр приложения
    app = QApplication(sys.argv)
    # Создаём базовое окно, в котором будет отображаться наш UI
    window = QWidget()
    # Создаём экземпляр нашего UI
    ui = MainWindow(window)
    # Отображаем окно
    window.show()
    # Обрабатываем нажатие на кнопку окна "Закрыть"
    sys.exit(app.exec_())




