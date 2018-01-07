# from os import popen
from subprocess import Popen, PIPE
from datetime import datetime
import time

from mysql.connector import MySQLConnection, Error
from PyQt5.QtCore import QDate, QDateTime, QSize, Qt, QByteArray, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request


from lib import s, l, t, read_config
from lib_scan import p, wj, wr, crop_tags
from mNote_env import LINK, PEOPLE, ONLINE, ISHTML, B
from mNote_win import Ui_Form

BREAKED_MAMBA = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xe1\x00*Exif\x00\x00II*\x00\x08\x00\x00\x00\x01\x001\x01\x02\x00\x07\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00Google\x00\x00\xff\xdb\x00\x84\x00\x05\x03\x04\x08\x08\x08\x08\n\x08\x08\x08\x06\x08\x06\x07\x08\x08\x07\x07\x07\x07\x07\x08\x08\x08\x08\x07\x08\x08\x08\x08\x07\x08\x08\x08\n\x10\x0b\x08\x08\x0e\t\x08\x08\r\x16\x0e\x0f\x13\x11\x16\x13\x13\x08\x0b\x16\x18\x16\x13\x18\x13\x12\x13\x12\x01\x05\x05\x05\x07\x06\x07\x0f\x08\x08\x0f\x18\x15\x12\x15\x1a\x1b\x17\x1d\x18\x17\x1d\x17\x18\x17\x18\x17\x18\x18\x17\x1a\x1d\x17\x1d\x17\x18\x1b\x17\x1d\x1d\x1d\x1d\x17\x1d\x19\x17\x18\x1d\x16\x15\x1d\x17\x15\x17\x17\x1d\x1d\x1d\x17\x17\x17\x17\x1d\x17\x1d\xff\xc0\x00\x11\x08\x01,\x01,\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1b\x00\x01\x00\x03\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x07\x08\x04\x03\x01\xff\xc4\x00<\x10\x00\x01\x04\x01\x02\x04\x04\x03\x05\x05\x07\x05\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x11\x12\x06\x07\x13!\x08\x141A\x15"Q#2aq\x815bu\x91\xb4$3BDRc\x82\x167t\xa1\xb3\xff\xc4\x00\x1c\x01\x01\x00\x02\x03\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x05\x03\x06\x07\x02\x01\x08\xff\xc4\x00?\x11\x00\x02\x01\x03\x02\x04\x03\x06\x03\x06\x04\x05\x05\x00\x00\x00\x00\x01\x02\x03\x04\x11\x05!\x06\x121QAaq\x07\x13"\x91\xa1\xb1\x14\x81\xc125s\xb2\xd1\xf0\x154Br\x16#S\xc2\xe1$3Rb\xa2\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xec\xb0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\xff\x00\x8a\xecq-<\x83\xe5\xa1V\x1e \xc7X\x864n=\xf6j\xd0\x9e\x9c\xf1\xa6\x8e{,H\xcf\xb5\x89\xfe\xaa\x8eW.\xab\xa2mD\xef\x06\xac\xaeaS\x9a\x9aR\x8b\xf0\xcaM?Sg\xd3\xe9hwvj\x95\xd4\xe5F\xac[\xcc\xd2\x94\xe38\xbe\x89\xc5=\x9a\xe9\xb2K\x1b\xbc\xbe\x92<\xbefm\xcd\xb56e\xd0\xc4\xfbS"\xd4\xc7W\xe8\xc8\xca\x101\xaa\x9b\x16\xc3\x18\x8e\x9eW\xaa\xea\xaa\xaa\xe4M\xa9\xa6\x9a\xaa&[o~\xd3uq\xd7d\xbc\x17\xa9\x0bZz\\]:ZrmE|S\x96S\x9c\x9f\x8a\x8bxItXI\xef\xbeq\x97o$\x94\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe6\xb7a\x90\xc6\xf9%{!\x8e\x16:I%\x91\xcddq\xc6\xc4W:G\xbd\xdd\x98\xc4DUU^\xc8\x88|\x94\x92Y{#\xd5:s\xab5\x08&\xdbi$\x96[od\x92[\xb6\xdfDx\xb0\x9cAF\xf7S\xc9]\xa9\x90\xe8\xed\xeb-;PX\xe9\xef\xdd\xb3\xa9\xd2z\xec\xd7k\xb4\xd7\xd7j\xfd\x0f\x14\xea\xd3\xa9\xfb\x12O\xd1\xa7\xf6$\xdd\xe9\xd7vX\xfcM)C9\xc72\x94s\x8cg\x19K8\xca\xce:e\x12\xc6B \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0eW\xe6\'\x1efx\x8f4\xecN\x0eg\xd5\xac\xc9\xa4\x81\xab\x0c\x8e\x87\xaf\xd0\xdd\xd7\xb5bf|\xc9]6\xb9Q\xa9\xea\x9avW*!\xad\xdc\xddV\xba\xad\xeeh\xbd\xb3\x8e\xd9\xc7V\xdfc\xb6h\x9c?\xa6h\x1aZ\xd4\xf5(\xa9O\n[\xaen^n\x91Q{gu\x96\xfc|RY$\x99\xe1\xb6\xf3\x1a\x92\xc5\x9dkn"k\xda\xb4\xecn\xff\x00\xfc\x96\xce\xaf\xf5\xf7\xd9\xfa\x19?\xc1f\x96T\xf7\xf4\x7f|\xfe\x847\xed:\xd2r\xf7s\xb5\xcd?X\xb7\x8f\xf6\xe3\x1f\xfe\x8d!q\xf9\n\x9c\x19\x90\x83+*\xd9\xbd\x06\x1b2\xd9\xe7t\xcb:\xc8\xdd\x97:\x0e\xea\xafw\xfd\x87K\xd7\xbf\xd7\xbe\xa4\xfeJ\x90\xb2\x94j\xbd\xf9^\xfd{\xe3\xe8i\xea\xe6\xce\xe7\x89\xe9U\xb1\x8f-7V\x93K\x1c\xb8\xde\x19X[/\x8b=6\xed\xb1\xce\\\x92\xe5o\xfdK\xe7\xbf\xb7|;\xe1\xdeW\xfc\xa7\x99\xeay\xaf1\xfe\xfb6i\xd0\xfcu\xdf\xed\xa7z\x0b\x0b\x0f\xc5\xf3|X\xc6<3\xd7>k\xb1\xd7\xf8\xaf\x8a\xff\x00\xe1\xefu\xff\x00+\x9f\x9f\x9b\xfd\\\xb8\xe5\xe5\xf2\x96s\x9f,`\xd6\xb8[\xc3\x8f\x91\xbfJ\xdf\xc6z\xff\x00\x0f\xbbZ\xd7K\xe1\x9d>\xa7\x96\x99\x92\xf4\xf7\xf9\xb5\xd9\xbbf\x9a\xe8\xbak\xe8\xa5\xa5-\x1b\xdd\xce3\xe7\xe8\xd3\xe9\xd9\xe7\xb9\xa1\xea>\xd2\xff\x00\x1biV\xdb\xf0\xd8\xe7\x8c\xa1\x9e|\xe3\x9a-g\x1c\x8b8\xceq\x95\x9e\xe4\xf7\x89Nd\xcd\x85\xad\rj.F^\xc8\xb5\xee\xeb\xe8\x8eZ\xd5\xe3\xd1\xae\x91\xa8\xee\xddW9tj\xae\xbalz\xfa\xe8g\xd5/]\xbcTa\xd5\xf8\xf6EW\x02p\xc5-b\xb4\xab\xdc\xac\xd3\x866\xff\x00\xe5\'\xbe\x1f\x92[\xbe\xf9^\x193\xbe\x1b\xe4V_1Z;\xb9<\xb3\xebMm\x8d\x9a8\xe7d\xd7g\xd9"ob\xca\xf7\xcc\xce\x93\x95\x1d\xae\x89\xae\x9a\xf7\xd1uD\xaf\xa5\xa5U\xaf\x1ez\x93\xc6w\xdfw\xf76\xdb\xfe?\xd3\xb4\x9a\xee\xd2\xca\xddJ1|\xad\xc5\xa8G+g\x84\x93\xca]\xf6\xcf\x86\xdb\x91\xd1g3\xdc\r\x95\x8a\xbd\xcb\x0f\xc8c\xe4F\xc9\xd2\xea>H\'\xac\xe7lt\x95\xfa\xbd\xeb\xce\xdd\x1d\xd94\xee\x8d\xd7V\xaa*\xe3\xf7\xb7\x1au^Y<\xc5\xfc\x9a\xf2\xec\xc9\x92\xb0\xd28\xcfO\x95{x(UYY\xc2R\x8c\xb1\x94\x9e:\xa7\xdf\xb7L4\xd1\xb4x\x8e\xb0\xc9xK#$nG\xb2fc\xe4\x8d\xc9\xe8\xe6?!M\xcdT\xfc\xd1S\xf9\x97\x1a\x9c\x93\xb3\x93^_ts\xae\x06\xa7*\\EF\x13Xi\xcd5\xd9\xa8M2\xb9\xe0\xfef\xc7\xc3\xf7\x9e\xf7#\x19\x1e^\xcb\xde\xe7.\x88\xd6\xb2\x8d\x079\xea\xbe\xc8\x88\x8a\xa4}\x15\xe2\xdeM\xf7\x7fd[\xfbM\x84\xa7\xacR\x8cwn\x9aIwns\xc20^o\xe6\xece\xefK\x93{\\\xda\x97l\xcfW\x1d\xbb\xb6\x90\xd0H~To\xb7k\x11\xb9\x7fzW\xfd\nK\xca\xb2\xaf7Y\xf4m\xa5\xe8\xb1\xfdN\xa5\xc364t\xbbH\xe9\xf1\xfd\xb8\xa5)\xff\x00\xba|\xdf\xaaiy$vG+?`\xe1?\x82\xe3\x7f\xa3\x84\xda\xed?\xcb\xc3\xd1}\x91\xf9\xef\x88\xbf{\\\xff\x00\x16\xa7\xf3\xc8\x93\xe2\x0c\x9ct\xaaZ\xb5+^\xf8\xa8U\x9e\xcc\xad\x8d\x11dX\xeb\xc4\xf9^\x8cETEz\xb5\xab\xa6\xaa\x89\xaf\xba\x19\xaaMS\x83\x9b\xf0M\xfc\x88\x16V\x93\xbb\xb8\x85\xbc1\x99\xc9Eg\xa6d\xd2Y\xc2o\x19{\xec\xfd\x0c\xd7\x19\xcf\xec\x0c\xd5\xadN\xef9U\xb4\xdd\x03:V!\x83\xada\xf6\x12g1\x95\xe3\x86g\xee\xd1 v\xe5r\xb5\x13Vw\xeeWGV\xa1(\xb9n\xb1\x8e\xb8\xcb\xceza\xbe\xc6\xe5q\xec\xf3W\xa3^\x14W,\x9c\x93y\x8b|\xb1Q\xe5\xcbm\xc68\xea\xb0\x96[\xdfm\x89\x1e\x18\xe7V\x06\xf4\x16fK\x0f\xa2\x94#\xea\xcf\x15\xd8\xdb\x1c\xbd%sX\x8f\x8d\xb1=\xe9.\xaf{\x1b\xa3UWW7\xb7t2\xd2\xd4\xa8T\x8by\xc6;\x90\xf5\x0e\x06\xd5\xec\xaa\xd3\xa5\xc8\xa7\xce\xf0\x9c\x1eVq\x9c<\xa5\x8d\x93yi,\'\xbe\xcc\xf2\xf0\xb7=\xb09\x0bq\xd5c\xadV\x92g\xa4P\xcbn\x08\xe3\x86Y\x1c\xbbX\xc4|r9\xccUwd\xdc\x8d\xf5<R\xd5(U\x97"\xca\xcfu\xb1\x9fP\xe0\rZ\xc6\xdd\xdcK\x96I,\xb5\x16\xdc\x92]^\x1aY\xc7\x8e\x1b.\\u\xc5\xf4p\xb5\x9bg!#\xe3\x85\xf36\x08\xfaq>W>W2I\x11\x88\x8cN\xdf$R.\xab\xa2|\xbe\xbe\x84\xba\xf7\x10\xb7\x8f4\xf6\xf05\xed#F\xba\xd6.?\x0fj\x93\x92\\\xcf-$\x92ig\x7f6\xbae\x99\xcb|I`\x15\xfbz96\xa2\xae\x9dE\xad[b~:%\x8d\xff\x00\xfa+\xff\x00\xc6\xad\xf3\xd2_%\xfdM\xc1\xfb2\xd6\x14s\xcdO=\xb3,\xff\x00.>\xa6\x9d\xc2|GO)U\xb6h\xce\xdbPH\xaa\xdd\xedEk\x9a\xf6\xe9\xba9\x18\xe4GF\xf4\xd5;*\x7f\x89\x17\xd1P\xb3\xa3Z\x15\xa2\xa5\x07\x94i\x1a\x8e\x9bs\xa6\xd7v\xf7Qq\x92\xf0\xee\xbb\xa6\xb6i\xf7_r\x91\x1f;\xb0\xc9\x93\xb1\x8f\x95\xb6\xea\xc9Jk\xb0\xcfjx\xeb\xb6\xa3W\x1e\xd9\x9d+\xb7\xb6u\x91\xcd^\x83\x91\xba3UUbh\x9a\x90\x7f\xc4\xe8\xfb\xd7M\xe5c)\xb7\x8cm\x9c\xf8\xf9m\xb1\xb3>\x04\xd4\xff\x00\x01\x1b\xd88\xc9MFJ1r\xe6|\xee),8\xa5\x95\x95\x9f\x8b\t&\xf2~p\xcf<\xf09\x0b\x8d\xaa\xc9,V|\xaf\xd9\x0c\xd6\xe1dpL\xf5\xfb\xadk\xdb"\xab5\xf6\xde\x8d\xfaz\xae\x82\x96\xa9B\xac\xf9\x13k=3\xd1\xff\x00~g\xddC\x80u{\x1bgq%\x19$\xb2\xd4[rK\xcdag\x1e<\xad\xfc\x8f6K\xc4\x0f\x0fAe`\xdfn\xcbZ\xed\xae\xb7^\xbb\x1fY\x15\x17G*9\xd2$\x8fj}Z\xd5E\xf6\xd4\xf3-^\xda2\xe5\xcb\xf5Ko\xef\xf22\xd0\xf6s\xac\xd6\xa1\xefq\x14\xda\xca\x8c\x9bR\xfb4\x9f\x93\x92\xc7\x8e\x0bo0n\xc5g\x872\xd3@\xf6\xcd\r\x8c\x0eBXeb\xea\xd7\xc6\xfaS9\xafo\xe6\x8aI\xb9\x9cgm)Gt\xe2\xfe\xcc\xa3\xd1hT\xb7\xd6\xed\xe9UMJ5`\x9a}SSYG=xb\xe3*\x18J\xd9\xc9\xef\xcc\xb15\xee\xc62(\xd8\xdd\xf3L\xfd2\x0e\xd9\x14i\xeb\xa3}UtD\xf7T\xd5\n=*\xe2\x9d\xbcg)\xbe\xde\xaf\xa9\xd5\xf8\xff\x00E\xbc\xd6+Z\xd1\xb4\x8eZ\xf7\x8d\xb7\xb4b\xbe\r\xdb\xfe\xdb\xf0F\xd9\xcb\xfeq\xe1s6\x12\xb5w\xcfR\xcb\xf5\xe9Cv&F\xb3h\x9b\x95"tr=\x8a\xed\x13]\xaa\xa8\xbak\xa2vR\xde\xdbQ\xa3q.X\xe7=\x9f\x89\xcd\xf5\x9e\x0b\xd54\x8a>\xfe\xb2\x8c\xa2\xba\xb86\xf1\xea\x9aO\xf3\xc6<\xc9\x9ebs\x07\x1b\x81l\x0e\xc8>V\xad\xce\xaf\x97\x8e\x18_#\xa4\xe8\xf4\xfa\x9a/f7N\xac\x7fyS]\xdd\xbd\x14\xcbswJ\xd9.\x7f\x1e\x9bv+\xf4N\x1d\xbe\xd6\xe5%j\x93Q\xc6[i%\x9c\xe3\xcd\xe7\x0f\xa2}\n=O\x12\x1c>\xf7\xa3]\x1eJ\x06\xaa\xe8\xb2\xc9V\x05b~*\x91N\xe7\xe9\xf94\x86\xb5\xab~\x98\x7fO\xeal\xd5=\x99\xeb\x10\x83\x92t\xdb\xec\x9c\xb3\xf5\x8a_SW\xc2\xe4\xe0\xbb\x04S\xd5\x95\x96k\xd9f\xf8\xa6\x8duk\x9a\xbd\x97\xf1G"\xa2\xa2\xa2\xf7Ej\xa2\xe8\xa8Z\xc2q\xa9\x1eh\xf4f\x89ukZ\xd2\xb4\xa8W\x8b\x8c\xa2\xf0\xd3\xea\xbf\xbf\x07\xd1\xad\xd1 z0\x19\xc72\xb9\xbb\x8d\xc0[\x8e\xad\xc8/K,\xd5Ye\xae\xab\x15w\xc7\xb1\xf2\xcd\x125VY\xd8\xa8\xfd\xd0\xbf\xdbM\x15;\xfd \\\xea\x14\xad\xa7\xc9<\xbd\xb3\xb6<\xfc\xd7cl\xd0x6\xfb\\\xb7w\x16\xf2\x82JN?\x13\x92yJ/\xc22X\xc3^=\xf6>6y\xd3\x84nN\x0ctN\xb1v\xc5\x8b\x91S\xebU\x8a7Vd\xf3J\x90\xb5\x1d+\xe4n\xe6#\xdd\xdd\xccG\'\xae\x9a\x9e^\xa5AU\xf7K-\xe7\x1bt\xcfO\xef\x06J|\x0f\xaa;\t_TQ\x8cT\\\xf1&\xd4\x9cRod\x93\xc3il\xa4\xd7\x9e\x0f\xae\x17\x9b\xb8\xdby\xa7b#\x82\xf3n2\xd5\xca\xcb,\x91WJ\xdb\xe86gJ\xa8\xf6\xce\xaf\xd8\xbd\x07i\xf2k\xdd5D\xf6\xfb\rF\x94\xeb\xfb\x84\x9er\xd7\x866\xcf\x9f\x97c\x1d\xd7\x06\xdfZ\xe9kT\x9c\xa1\xee\xdcc,\'.lM\xc5-\xb9R\xca\xca\xcf\xc5\xe8\xd9\xef\xe6\x8f2\xe8p\xea\xd4\xf3\xb1\\\x9b\xe2\x1d~\x97\x93\x8e\x07\xed\xf2\xdd\x1d\xfdN\xac\xcc\xd3^\xbb4\xd3_E\xf4\xf7\xc9w{\x0b\\s\xa7\xbezc\xc3\x1d\xda\xeeF\xe1\xee\x17\xbb\xd7\xbd\xe7\xe1\xa5\x15\xc9\x8c\xf3\xb9/\xda\xe6\xc60\xa5\xd9\xe78\xf0,\xfc?\x93\x8e\xedJ\xb6\xa2k\xd9\x15\xfa\xb0Y\x89\xb2"$\x89\x1d\x88\x99+\x11\xe8\x8a\xa8\x8fF\xb95\xd1U5\xf7RM9\xaa\x90S^)?\x99Iyi;K\x89\xdb\xcf\x19\x84\x9c^:f-\xa7\x8c\xa4\xf1\x95\xb6\xcb\xd0\x92=\x91\xc0\x00\x00\x01\xc7\xfe\x1cmG\x8a\xe2\x99\xa0\xbc\xa9\x0c\xb2\xc5o\x1e\xd7J\xbbQ-6\xc4NF\xaa\xbb\xee\xb9\xdd\x07\xb5>\xaa\xf6\xa7\xb9\xaa\xe9\x8dQ\xbb\xe5\x9f\x9a\xfc\xf2w\xce9\xa5=K\x87\xe3Z\xd9e\'\x1a\x9bo\xf0r\xb5\xf4\xcao\xb2Y\xf0;\x00\xda\x8e\x06T\xf9\x93;$\xc0f\x9c\xc7\xb6V\xfc\x1f*\xdd\xccr=\xba\xc7Z\xc3\x1c\xdd[\xee\x8ej\xa2\xa7\xb2\xb5S\xd8\x8ft\xd3\xb7\x9b]\x9f\xd9\x97Z\r9S\xd6-c$\xd3\xf7\x94\xde\x1a\xc6\xceQk\xe6\x9ak\xba\xdc\xe5\x0eIr\xb7\xfe\xa5\xf3\xdf\xdb\xbe\x1d\xf0\xef+\xfeS\xcc\xf5<\xd7\x98\xff\x00}\x9b4\xe8~:\xef\xf6\xd3\xbe\xafaa\xf8\xbeo\x8b\x18\xc7\x86z\xe7\xcdv;\xaf\x15\xf1_\xfc=\xee\xbf\xe5s\xf3\xf3\x7f\xab\x97\x1c\xbc\xbeR\xces\xe5\x8c\x12\x19W\xe58\x1f7\x0c1d\x1fr\x1d\x90\xd8|MW\xb6\x1b\x15\xe5\x91\xectr\xd5W\xb9\x19/\xd9\xc8\x88\xa8\xaa\xa9\xaa*/s\xdc\xdd]:\xb7*\x96V\xcf\xc9\xafB\x1d\xba\xb0\xe3-.U\xa7EFYqM\xe1\xca2I4\xd4\x92M\xad\xd7d\xf7M\x13\xfe3\xe9H\x99L|\xea\x8b\xd2\x9b\x1b\xd1b\xfbu \xb33\xe4O\xcfm\x88L\xfa\xdc_\xbd\x8c\xbc\xb1\xf2o\xfa\x95\x9e\xcbkA\xd8V\xa2\xbfiO\x99\xfaJ1K\xea\x99\xd2\xdc/\x96\x82\xf5:\xd6k9\xaf\x82\xd4,\x925j\xa2\xa2"\xa7v.\x9e\x8ej\xea\xd5Oej\xa7\xb1\xb1R\x9cjAJ=\x1a8\xcd\xfd\xa5[;\x99\xd0\xac\x9a\x94[O?\x7fG\xd5?\x15\xb9\xce\x1e2\xf2\xb0Kw\x1bZ75\xf3\xd2\x86\xcb\xec#WUb[t\x1d(\xdd\xa7\xddv\x90\xbd\xdaz\xe8\xf6\xaf\xba\x14\x1a\xe5H\xb9\xc6\x0b\xaaO?\x9e1\xf6;\x07\xb2\xebJ\xb4\xad\xab\xdcMb3qK><\xbc\xd9k\xcbt\xb3\xdd5\xe0h<\xe0\xa9%~\x01t2\xa2\xa4\xb5\xb1\xb8X\xa5E\xf5I"\xb3\x8fc\xd1\x7f\xe4\xd5&\xde\xc3\x93O\xe5}RK\xea\x8dW\x86k\xc2\xbf\x17\xaa\xb4\xfaJud\xbd\x1cf\xd7\xd0\xc6\xf8/\x88f\x8f\x85\x1f\x8b\xa5\xab\xef\xf1/\x10MR65trWu\\rL\xab\xfe\x94{\x9c\xc8\xfb\xf6\xda\xf9>\x85M\n\xd2V\x8e\x94?jRk\xf2\xc2\xcf\xf4\xf9\x9d\x0bT\xd3i\xcf\x88\x16\xa3q\xb5:\x14T\xdb\xff\x00\xed\xcdQ\xaf\x96\x1c\xbdR\xeeMx\x9e\xe1\xd8\xb18\xee\x18\xa5\x0fvS\x87$\xd7?M\x16I]\xf0\xf7\xcb2\xfe\xf3\xa5s\xdd\xfa\xe8f\xd5hF\x8d:t\xd7\x86\x7fL\x95\xde\xcf\xf5*\x9a\x9d\xed\xf5\xddN\xb2t\xde;/\x8d%\xf9,#\xa2yY\xfb\x07\t\xfc\x17\x1b\xfd\x1c%\xed\xa7\xf9xz/\xb29/\x11~\xf6\xb9\xfe-O\xe7\x90\xe6\x9f\xec\x1c\xdf\xf0\\\x97\xf4s\x0b\xbf\xf2\xf3\xf4\x7ff8w\xf7\xb5\xb7\xf1i\xff\x00<L\x17\xc1~2\x19le\xa7|m|\xb5b\xa7\x14.sQU\x8d\xb4\xb6\x96m5\xf4\xd7\xa2\xc4\xfc\xb5\xfa\x94\xda\x1c\x14\xa59>\xab\x1f\\\xff\x00C\xa7\xfbS\xb9\xabN\x8d\xbd\x18\xb6\xa3\'&\xd7w\x1e\\g\xd3,\xab\xf06\x1a\xbc\xdcz\xfa\xcf\x89\x8e\xaf\x16o,\xac\x85Z\x8b\x1a%?;4,\xd9\xe9\xb5\x1d\x13;z|\xa4[zQ\x96\xa0\xe2\xd6\xdc\xcf\xe9\x96\xbe\xc5\xde\xaf{Z\x97\x08+\x88\xc9\xa9\xbaT\xf2\xf3\xbf\xc5\xc8\x9b\xcfv\x9b\xdc\xf6x\xbb\x89\xb0\xf1\x05g\xc4\xd6\xc4\xf91U\xa5s\x98\x88\xd5Y[j\xe3\x12Gi\xfe-\xb1\xc6\x9a\xfe\xe2\x1e\xf5\x94\xa3p\x9a\xec\x9f\xd5\x91\xfd\x9aM\xd5\xd1\xe7\t\xbc\xa5RI\'\xe0\x9c`\xf1\xe9\x96\xdf\xe6n<\xf6\xe3\xba\x98:\xb5\x9f=8\xf2v,L\xf5\xa5^dn\xc6>\x16i%\x85{\x98\xe5f\xc6\xcc\x89\xf2\xa6\xab\xd4\xd3TEU.\xaf\xee\xe1o\x05\x95\x96\xde\xcb\xf59\xa7\x08p\xfd\xc6\xb3q8\xd3\xa8\xe9\xc6)sIg-7\xb4p\x9a\xceZ\xce\xfb,gw\x83-\xe2~(\xe2\xec\xbe\x12\xcc\xb3`q\x89\x89\x9a\x8c\xb2\xad\x89\x11\x1b$P67?\xcd\xc0\xc9\xaf#\xfa\x8djoj\xa3\x17UD\xd1\x17]\x16\xb2\xad\xc5\xe5j\r\xb8G\x97\x19\xcf\x97u\x97\xf2\xd8\xdd\xac4\xae\x1c\xd2\xf5XS\xa7wS\xdf\xa9(\xf2\xad\xd3\x96q\xca\xdc`\xd6\x1b\xdaI\xc9c|\xb4{|\x14Xr\xc7\x9a\x8dWVG&>F\xb7\xd9\x1f+n5\xee\xfdR(\xff\x00\x92\x1e\xf4&\xda\x9a\xf4\xfdH\xfe\xd5\xa1\x15R\xdak\xabSO\xd1r5\xf7\x7f2\x99\xc28\xe8m\xf3\nx\xa7ce\x8ds\xf9\x99U\x8fDTWW[\xb3\xc7\xb9\x17\xd57\xc4\xc5\xd3\xf0!\xd1\x82\x9e\xa0\xd4\xbas?\xa6Y\xb1jw5-\xb865)<?uIeu\xc4\xb9"\xfe\x8d\x9f_\x185\xa3\x8f?\x02\xb1\x8db\xcd\x89\xaf$\x8a\xd4D\xde\xff\x003n=\xeb\xf5]\x91\xb1?&\xa1\xebZIW^\x8b\xee\xcc~\xccj\xcezD\xd4\x9eR\xa8\xd2\xf2\\\xb0x\xf9\xb6\xff\x002\xf9\xe2\xbf\x0bZ\xa7\x0fc#\x82(\xe2m,\x94\x15\xe0V\xb5\xadV\xc4\xeav\xd5\xec\xd7\xf7\x96(\xd5~\xaa\xddT\x9b\xab\xd2\x8c-\xe2\xa2\xba4\xbe\x8c\xd5\xfd\x9c\xdfW\xba\xd6\xab\xce\xa4\x9bs\x83\x93\xcb\xea\xf9\xa1\x87\xf9e\xa5\xd9lJr\xf5\xea\xee\\\xcc\xae]U0y\xd6\xa6\xbfF? \xc6\xa7\xe8\x8dD2[~\xed~\x92\xff\x00\xb8\x85\xad\xc5G\x8d\xa2\x97\xfdZ?UM\xb2\x91\xe0\xcb\x1b^Ky9\xe4c\x1fb\xa45[Y^\xd6\xb9\xccl\xee\xb1\xd7s5\xfb\xae\xfb(\xd3T\xef\xa2\xaa{\x9148E\xceRku\x8c~y6OjwU\xa9\xdb\xd0\xa3\x06\xd4d\xe4\xde<\\Tp\x9f\xcd\xbcyy\x10\xfe%ae\x0e)\xaf5\x16\xa43\xbe\n\x97\x1c\x90\xa25|\xe3lL\x8d~\x8d\xf4z\xb6(U~\xaa\xed}\xcc:\xacU+\xa5(u\xc2\x7f\x9eYa\xc0u%}\xa0N\x95\xd3\xccT\xa5\r\xf7\xf89b\xf1\xbf\x82\xcb^_\x91\xae\xf3\xef\x99\xd5\xf0R\xd5\x8d\xb4 \xc9d\x1f\x13\xe6\x85\xd6\x11\xbbj\xc2\xf7\xecW\xb5\xdbU\xeet\x8f\x87M\xadV\xff\x00u\xaa\xafdB\xd3Q\xbe\x8d\xbbI$\xe5\xd7\x7f\x05\xff\x00\x93B\xe0\xde\x16\xaf\xadS\xa9Q\xd5\x95:YQj=e$\xb3\x8cg\x1b\'\xd5\xa7\xd7e\xd4\xcdy\xbb\x96\xe2\xcb\xd8id\xcb`\xf1\xd4\xa8"\xd7\x91\xb6\xd3km\xd7WM\x1bc\xe9\xb1\xf7]#\x1c\xe79\x18\xa9\xd3\xfb\xb2?TOT\xaf\xbd\xa9wR\x8ej\xc1(\xf7\xf1[\xfa\xe7\xe8n<5g\xc3\xd6Z\x9caauRU7\\\xbf\xe8\x96"\xf3\x96\xa0\x93K\x19_\x17T\xba\xf4w\xff\x00\x07\x96\x1e\xfc\x04\xeds\x95\xc9\x06Z\xc4q\xa2\xaf\xddb\xd6\xa9*\xb5?\xe7#\xd7\xf5&\xe8\xaf\xff\x00N\xfd_\xd9\x1a\xb7\xb4\xdaq\x86\xb1\x16\xba\xbaqo\xcd\xf3M}\x926\xa2\xe0\xe7g$x\xcb\xfd\xbdS\xf8$\x1f\xd6_5mk\xfc\xc2\xf4_vw\x8fe\xff\x00\xbaj\x7f\x15\xff\x00,\r\xfb\x86y]\x84\xa3\x05F7\x1fY\xf3Qt\x136\xeb\xe2j\xda[09\x92$\xfd\x7f\xbe\x9fh\xdd\xdbQv\xfbi\xa7b\xf6\x95\x8d\nib++\x1b\xf8\xe5x\xe4\xe5Z\x87\x15\xea\xb7\x95jJU\xa4\xa3,\xaeT\xfe\x0eYer\xf2\xf4\xe8\xf1\x9cg\xc79\xdc\xc0yo\xff\x00q\xe6\xfe5\x9f\xff\x00\xe5\x92(\xed\xbfy?Y\x7f\xdcuMs~\n\x8e?\xe9Q\xfb\xd3,>6dn\xec#Q~f\xb7"\xe77\xdd\x1a\xf5\xa2\x8d_\xd5X\xef\xe4g\xd7_\xec~\x7f\xa1S\xec\xa6-+\xa9cg\xee\xd7\xcb\x9f\xfa\xa3q\xe5g\xec\x1c\'\xf0\\o\xf4p\x97\x16\x9f\xe5\xe1\xe8\xbe\xc8\xe6\xbcE\xfb\xda\xe7\xf8\xb5?\x9eE\x94\x92T\x00\x00\x00\x03"\xe6\xf7$\xe9\xe6\xe5u\xaa\xf3|6\xfb\xda\x89,\x89\x1e\xf8,mM\xa8\xe9X\x8a\x8el\xba#Sz/\xa2wE*\xeft\xc8\\>x\xbc?\xa37\xae\x19\xe3\xab\x8d\x1a\x9a\xb6\xab\x1fyMtY\xc4\xa3\x9e\xcf|\xaf\'\xf94Q[\xc9.,sz2q\x0b|\xa6\x9bzi\x91\xca\xbd\xbb\x7f\xd3\xe5\xdd\x1a3\xd3\xdbR\x17\xf8e\xdb\\\xae\xa6\xde\xb2\xfb\x1b;\xe3\xae\x1d\x8b\xf7\xd0\xb3|\xfds\xc9M<\xff\x00\xbb-\xfex5\xacW\x02\xbe\x97\x0cM\x87\x86\xc2Y\x91\xd8\xec\x85X\xec\xca\xd5\x85\x8e\x96\xff\x00\x99r9\xecf\xf5dh\xfb\x1av\xdc\xba7\xddKHZ\xfb\xbbWE<\xec\xd6}s\xeb\xdc\xd0\xee5\xf8\xdd\xeb\xb1\xd5*E\xa4\xa7\t8\xa7\x97\x88r\xac&\xf1\x96\xd2\xf2Y\xecb\xf8NDqe\x1d\xfeK1S\x1f\xd7\xdb\xd6\xf2y,\xad~\xa6\xcdvu:US~\x9b\x9f\xa6\xbe\x9b\x97\xeaS\xd3\xd2\xae\xe9\xfe\xc4\xd2\xf4r_dt[\xbe?\xe1\xeb\xdc~&\xdeS\xc6q\xcf\nr\xc6q\x9cfO\x19\xc2\xce:\xe1\x13\xdc\x1d\xe1\xfa\xd2\xde\x8e\xe6w"\xdc\x8b\xa3\x95\xb2\xbe(\x9dbwXs\x15\x15\xa9=\x9b\x08\xd7\xec\xec\xddSj\xaa\xa7mP\x91KH\x9f\xbc\xe7\xaf,\xfc\xde\x7f6U\xea\x9e\xd1-\xd5\xa3\xb5\xd2\xe8\xb8&\x9aM\xa8\xc5E>\xd1\x8eV{<\xec\xf7\xc35\xeeb\xf0],\xed7V\xb8\xd5DGo\x82x\xf4I`\x95\x13jI\x1a\xaa}\x17EE\xec\xa8\xbf\x92\xa5\xa5\xcd\xb4.!\xcb/\xc9\xf64\r\x0f\\\xba\xd1nU\xc5\xbb\xf2i\xf4\x92\xec\xff\x00G\xd53\x10g!\xb8\x8e\x8a\xbd\x98\xac\xfb \x81\xeeUr%\xac\x8d\x17;\xf1|U\xd1\xecWi\xf8\x94\xebI\xb9\xa7\xff\x00\xb5=\xbdZ\xfbd\xe9r\xf6\x81\xa2^%;\xebF\xe4\xbc\xa1<z98\xbf\xa1c\xe5\xaf b\xa7i\x97r\xd6\x93+f)\x12V@\xc6\xbf\xa0\x935w$\xb3I/\xcfa\xc8\xbd\xf4Tjj\x9d\xf5\xf43\xda\xe9*\x12\xe7\xaa\xf2\xfbxg\xf5)\xf5\xefhu.\xed\xdd\xad\x85?w\x16\xb0\xe4\xf1\xcd\xcb\xd9%\xb2\xdbn\xafn\x984No\xf0\xd4\xf9\x8c-\xcaU\x9d\x14S\xdb\xf2\xdb\x1fa\xcflI\xd1\xb7\x04\xee\xde\xb1\xb1\xca\x9f$ND\xd1\x17\xba\xa7\xe6X^\xd0\x95z2\xa7\x1ce\xe3\xaf\x93L\xd4\xb8cT\xa3\xa5j\x94\xaf+&\xe3\x1c\xe5G\r\xef\x19%\x8c\xb4\xba\xb5\xe3\xd0\xce9\x1b\xc9+8l\x8a\xdc\xc9KN\xcb\xa0\x85\xcd\xa4\xca\x8f\x9eDd\xb2\xfc\x92L\xfe\xb4,\xda\xa9\x16\xadM5\xfe\xf5W\xb6\x88Wi\xfa\\\xa8T\xf7\x95\x1ax\xe9\x8c\xfe\xa9\x1b\x7f\x16\xf1\xd5\rZ\xcb\xf0\x96q\x9cSi\xc9\xc9Ee-\xd2Xr\xf1\xdd\xf4\xe9\xe3\x96M\xf8\x88\xe5\xa5\xfe"\xf8o\x92\x9a\xa4>C\xcd\xf5\xbc\xe4\x93\xb3w\x98\xf2\xbb:}(_\xae\x9d\x17\xeb\xae\x9e\xa9\xeb\xed\x9fR\xb2\xa9u\xcb\xc9\x8d\xb3\xd7>8\xec\x9fb\xbb\x82x\xa2\xd3A\xf7\xdf\x89\x8c\xdf?.9T_\xec\xf3g9q\xee\xb1\x8c\xf8\x9a\x17\x05\xe3$\xa5\x8d\xc7\xd5\x95Z\xe9hc\xeaV\x95\xd1\xaa\xacn\x92\xbc\x11\xc4\xf71\\\x88\xaa\xc5s\x17MQ\x17M;!>\x84\x1d:Q\x83\xf0I|\x91\xa9j\xb7P\xbb\xbe\xadq\x04\xd2\x9c\xe5%\x9e\xb8\x94\x9bY\xc3{\xe3\xae\xef\xd4q\xa62K\xb8\xdc\x85X\x95\xad\x96\xfe>\xddh\x9d"\xaaF\xd9,A$Ls\xd5\xa8\xaa\x8cG=5\xd1\x15t\xd7\xb2\x8a\xf0u)J\x0b\xc55\xf3CJ\xba\x85\xa5\xf5\x1b\x89\xa6\xd4\'\x19<u\xc4d\x9b\xc6Z\xdf\x1d7^\xa6{\xe1\xdf\x96\x97\xf8w\xe2^vj\x93y\xff\x00)\xd1\xf2rN\xfd\xbe_\xcdo\xeauaf\x9a\xf5\x99\xa6\x9a\xfa/\xa7\xbc\r6\xca\xa5\xaf7>7\xc7L\xf8g\xba]\xcd\xb7\x8d\xb8\xa2\xd3^\xf7?\x86\x8c\xd7\'6y\x94W\xedr\xe3\x18r\xec\xf3\x9cx\x11\x1c)\xca,\x95N,\x931$\xf4]Q\xf9\x0c\xa5\x96\xc5\x1c\xb6\x16\xcfN\xfb-\xb6$V:\x04f\xf4\xeb\xb7_\x9fN\xcb\xa2\xaf\xbe*:uJw~\xf9\xb5\x8c\xb7\xe3\x9d\xf3\xe5\xfa\x93\xb5\x1e2\xb1\xba\xe1\xe5\xa5\xc23\xf7\x8a\x14\xe3\x96\xa3\xcb\x9887\xbf3xxx\xf8{l\x87?yC\x92\xcf\xe4\xa0\xb5Nz0\xc5\x0e>*\xcem\xa9l\xb2E\x91\x96,\xca\xaejE\x03\xd3f\xd9\x9b\xef\xae\xad^\xdf_\x9a\x86\x9fV\xe6\xaa\x9c\x1a\xe9\x8d\xf3\xdd\xf93\xef\x06\xf1\x95\x8e\x87c+{\x88\xcd\xb77/\x85E\xac8\xc5x\xca/9O\xc3\xb6\xe5\xbb\x9d\xfc\xb6o\x11\xd5\x85\xac\x99*\xda\xa0\xf9\x1fZW\xb5]\x1a\xa4\xc8\xd4\x96\x19\x11>f\xb5vF\xbb\x93UEg\xa2\x93/\xec\x95\xd4\x16\x1e\x1a\xe8Pp\x97\x13\xcb@\xb8\x94\x9cy\xa14\x93Kg\xb6p\xd7\x9a\xcb\xd9\xf5\xcfTRq\xbc\xa7\xe2Y1\xb2\xd0\xc8g"}8\xa9\xcb\x15*5w\xa3\x1d+bsj2\xcd\xa7Wl\xbeU\x92\xf4\xd5Y\xa3\xfb3DB\x14l.]/wR{cd\xbe\x99x\xce>f\xc9_\x8b\xf4:w\xca\xf6\xd2\xd5\xfb\xc7$\xe59c)es5\x1ef\xb9\x9a\xcaOm\xderO\xf8w\xe5\xa5\xfe\x1d\xf8\x97\x9d\x9a\xa4\xde\x7f\xcat|\x9c\x93\xbfo\x97\xf3[\xfa\x9dXY\xa6\xbdfi\xa6\xbe\x8b\xe9\xef\x9fM\xb2\xa9k\xcd\xcf\x8d\xf1\xd3>\x19\xee\x97r\xaf\x8d\xb8\xa2\xd3^\xf7?\x86\x8c\xd7\'6y\x94W\xedr\xe3\x18r\xec\xf3\x9cx\x11\x1c)\xca,\x95N,\x931$\xf4]Q\xf9\x0c\xa5\x96\xc5\x1c\xb6\x16\xcfN\xfb-\xb6$V:\x04f\xf4\xeb\xb7_\x9fN\xcb\xa2\xaf\xbe*:uJw~\xf9\xb5\x8c\xb7\xe3\x9d\xf3\xe5\xfa\x93\xb5\x1e2\xb1\xba\xe1\xe5\xa5\xc23\xf7\x8a\x14\xe3\x96\xa3\xcb\x9887\xbf3xxx\xf8{l\x87?yC\x92\xcf\xe4\xa0\xb5Nz0\xc5\x0e>*\xcem\xa9l\xb2E\x91\x96,\xca\xaejE\x03\xd3f\xd9\x9b\xef\xae\xad^\xdf_\x9a\x86\x9fV\xe6\xaa\x9c\x1a\xe9\x8d\xf3\xdd\xf93\xef\x06\xf1\x95\x8e\x87c+{\x88\xcd\xb77/\x85E\xac8\xc5x\xca/9O\xc3\xb6\xe5\xb3\x9f\x9c\x0fo?\x8d\x82\xad9+\xc3,Y\x08\xac\xb9\xd6\xdf+\x19\xd3d\x16bTE\x8a7\xbb~\xe9\x99\xed\xa6\x88\xbd\xfe\xb2\xf5\x0bY\xdc\xd2\xe4\x8b[<\xef\xe8\xfd{\x94<\x1b\xaf[\xe8w\xd2\xb8\xb8Ri\xc1\xc7\xe1I\xbc\xb9E\xf8\xb8\xed\x84\xfc{l8S\x81\xed\xd4\xe191\x12I]\xd7\x1f\x8f\xc9\xd6Ic|\xcb[\xa9~KN\x89U\xee\x8d\x1f\xb1:\xec\xd7\xe4\xd7\xb3\xb4E\xf7Q\xb6\x9c-=\xcb\xc6p\xd7\x96\xf9\xf2\xf3\xec5\x1dz\xde\xeb\x88V\xa9\x05%\x05:r\xc3K\x9b\x10QOl\xb5\x97\x87\x8f\x8b\xb6Z3\xde^\xf2G9\x8aKsC\x96\xaf\x8e\xc8\xb9!m)\xaa,\xb6 |_i\xe6 \xb9\r\x8a\xedG5W\xcb\xabU\x11\xda,k\xd8\x81m\xa5\xd7\xa2\x9c\x94\x92\x96\xd8\xc6\xeb\xcd<\xafCm\xd6\xb8\xf3J\xd4\x9d:U-\xe5:[\xb9)b2OlJ.2o+\xe2Mee5\xb9#\xc1\xfc\x93\xbe\xfc\xb3r|E\x90\x8b\'4R\xb2f\xc5\x07U\xcd\x9aX\xb4\xe9,\xaf|lFD\xcd\xad\xd26\xb7E\xd1\x13\xb2j\x8b\xee\x8e\x9b7W\xde\xd7\x96_]\xbe\x9d\xbeD=O\x8e\xad!\xa7\x7f\x87\xe94]8\xb4\xe2\xdc\xb0\xb0\x9f\\$\xe5\x96\xf2\xf7o>=wS\xbc\xf8\xe5\x12\xf1\x0b\xa0\xb1Zx\xea]\xad\x12\xc1\xf6\xe8\xf5\x86h\xb7\xac\x8cc\x9c\xc4WF\xe6\xbd\xef]Q\x17]\xeb\xd8\xcf\xa8i\xff\x00\x89jQxkm\xfa4Vp\x7f\x18\xad\tJ\x85h9S\x93\xe6\xf8q\xcd\x19a&\xd6p\x9eR[et+\xf9\xaeS\xf1.K\x19,\x19L\xdc7f\x89\xb1&>\xb2,\x91\xd4k\xd9,{\xe7\xb7;+\xa4\xb6$J\xe93[\xb9\x8e\xf9\x9e\x8b\xa9\x82\xa5\x85\xcdZN5&\x9bX\xc2\xf0\xf5o\x19{y\x16\xb6\xbc]\xa1\xe9\xf7\xf1\xadej\xe3\x17\x9eyl\xe6\xd3O\x11\x8c\\\x9aK\x9b\r\xe2Ke\x8c\x17NA\xf0=\xbe\x1f\xc6\xcfV\xe4\x95\xe6\x96\\\x84\xb6Z\xea\x8f\x95\xec\xe9\xbe\n\xd1"*\xcb\x1b\x1d\xbft/\xf6\xd3EN\xff\x00I\x9a}\xac\xed\xa9rI\xad\xdev\xf4^\x9d\x8ds\x8c\xb5\xeb}r\xfa7\x16\xeaI((\xfcI\'\x95)?\x07-\xb0\xd7\x8f}\x8a\x9f\nr\x8b%S\x8b$\xccI=\x17T~C)e\xb1G-\x85\xb3\xd3\xbe\xcbm\x89\x15\x8e\x81\x19\xbd:\xed\xd7\xe7\xd3\xb2\xe8\xab\xef\x16\x8e\x9dR\x9d\xdf\xbemc-\xf8\xe7|\xf9~\xa5\xee\xa3\xc6V7\\<\xb4\xb8F~\xf1B\x9cr\xd4ys\x07\x06\xf7\xe6o\x0f\x0f\x1f\x0fm\x90\xe7\xef(rY\xfc\x94\x16\xa9\xcfF\x18\xa1\xc7\xc5Y\xcd\xb5-\x96H\xb22\xc5\x99U\xcdH\xa0zl\xdb3}\xf5\xd5\xab\xdb\xeb\xf3P\xd3\xea\xdc\xd5S\x83]1\xbe{\xbf&}\xe0\xde2\xb1\xd0\xeceoq\x19\xb6\xe6\xe5\xf0\xa8\xb5\x87\x18\xaf\x19E\xe7)\xf8v\xdc\xdd\x0b\xa3\x9a\x98\'\x1f\xf2S!&e\xd9L\x1d\xf8hO4\xfee\xcd\xb2\xb2\xb1b\xb0\xe4\xfbG\xc6\xf8\xe3~\xf6\xbdU\xca\xadst\xf9\xdc\x9d\xd1t).4\xca\x8e\xb7\xbd\xa3$\x9es\xbf\x83\xfa\x9d;F\xe3\x9b8i\x8bN\xd4\xe9JqK\x971\xc3\xccWD\xd3q\xc3[a\xa7\xe0\x9e\xcc\xf0s\x0f\x91\xf9\xbc\xaaU\x9a\\\xad|\x8eE\xa93n\xcfqe\xaf\x03c\xfb/-\x058k\xc0\xe4k\x1a\xef0\xaeUF\xea\xb2"\xe8x\xb9\xd2\xebV\xc4\x9c\x93\x96\xf9oe\xe4\x92K\xd4\x95\xa2q\xe6\x97\xa6\xba\x94\xa9\xdb\xca\x14\xb6qP\xc4\xa4\xde\xf9\x94\xa5)\'\x97\xf0\xa4\xb2\xf0\x97So\xe0\xbcd\x94\xb1\xb8\xfa\xb2\xab]-\x0c}J\xd2\xba5U\x8d\xd2W\x828\x9e\xe6+\x91\x15X\xaeb\xe9\xaa"\xe9\xa7d.hA\xd3\xa5\x18?\x04\x97\xc9\x1c\xd7U\xba\x85\xdd\xf5k\x88&\x94\xe7),\xf5\xc4\xa4\xda\xce\x1b\xdf\x1dw~\xa4\xd9\x94\x82\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xd9'

def authorize(driver, login, password, authorize_page=''):
    time.sleep(1)
    if authorize_page != '':
        driver.get(authorize_page)
    time.sleep(1)
    sel = p(d = driver, f = 'c', **B['select_in'])
    sel.click()
    # Ввод логина
    log = p(d = driver, f = 'c', **B['login'])
    time.sleep(1)
    log.send_keys(login)
    # Ввод пароля
    passwd = p(d = driver, f = 'c', **B['password'])
    time.sleep(1)
    passwd.send_keys(password)
    # Отправка формы нажатием кнопки
    cl = p(d = driver, f = 'c', **B['a-button'])
    cl.click()
    return


class MainWindowSlots(Ui_Form):   # Определяем функции, которые будем вызывать в слотах

    def setupUi(self, form):
        Ui_Form.setupUi(self,form)

        self.fillconfig = read_config(filename='mNote.ini', section='fill')
        self.messages = read_config(filename='mNote.ini', section='messages')
        self.webconfig = read_config(filename='mNote.ini', section='web')

        self.drv = webdriver.Firefox()  # Инициализация драйвера
        self.drv.implicitly_wait(5)  # Неявное ожидание - ждать ответа на каждый запрос до 5 сек

        dbconfig = read_config(filename='mNote.ini', section='mysql')
        self.dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
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
        self.fotos_count = {}
        self.names = {}
        self.ages = {}
        self.chk_educ = False
        self.chk_child = False
        self.chk_home = False
        self.chk_baryg = False
        self.chk_marr = False
        self.chk_dist = False
        self.history = ''
        self.histories = {}
        self.stLinkFrom = 2
        self.cbLinkFrom.addItems(LINK)
        self.cbLinkFrom.setCurrentIndex(self.stLinkFrom)
        self.stLinkTo = 7
        self.cbLinkTo.addItems(LINK)
        self.cbLinkTo.setCurrentIndex(self.stLinkTo)
        self.stPeopleFrom = 6
        self.cbPeopleFrom.addItems(PEOPLE)
        self.cbPeopleFrom.setCurrentIndex(self.stPeopleFrom)
        self.stPeopleTo = 9
        self.cbPeopleTo.addItems(PEOPLE)
        self.cbPeopleTo.setCurrentIndex(self.stPeopleTo)
        self.stStatus = 0
        self.cbStatus.addItems(ONLINE)
        self.cbStatus.setCurrentIndex(self.stStatus)
        self.cbPeople.addItems(PEOPLE)
        self.cbPeople.setCurrentIndex(0)
        self.cbLink.addItems(LINK)
        self.cbLink.setCurrentIndex(6)
        self.cbHTML.addItems(ISHTML)
        self.cbHTML.setCurrentIndex(2)
        self.setup_tableWidget()
        self.myTimer = QTimer()
        self.myTimer.start(300000)
        self.refresh_started = False

        return

    def click_pbPeopleFilter(self):  # Применить фильтр
        a = self.leFilter.text()
        if a[:4] == 'http':
            self.leFilter.setText(self.convert_mamba_id(a))
        self.setup_tableWidget()
        return

    def click_cbHTML(self):
        self.setup_tableWidget()
        return

    def setup_tableWidget(self):
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)        # Кол-во строк из таблицы
        self.dbconn.connect()
        read_cursor = self.dbconn.cursor()
        sql_append = ''
        if self.stStatus == 0:
            sql_append = 'AND status > 0 '
        elif self.stStatus == 1:
            sql_append = 'AND DATE(access_date) >= DATE_SUB(NOW(), INTERVAL 24 HOUR) '
        elif self.stStatus == 2:
            sql_append = 'AND DATE(access_date) >= DATE_SUB(NOW(), INTERVAL 3 DAY) '
        elif self.stStatus == 3:
            sql_append = 'AND DATE(access_date) >= DATE_SUB(NOW(), INTERVAL 7 DAY) '
        if self.cbHTML.currentIndex() == 1:
            sql_append += 'AND html IS NOT NULL ORDER BY age DESC;'# сообщения не показывает, с...
        elif self.cbHTML.currentIndex() == 0:
            sql_append += 'AND html IS NULL ORDER BY age DESC;'
        else:
            sql_append += 'ORDER BY age DESC;'
        if len(s(self.leFilter.text())) > 4:
            sql = 'SELECT DATE_FORMAT(access_date,"%d.%m %H:%i"), her_name, age, msg, fotos_count, id, msg_id, mamba_id,' \
                  ' t_people, t_link, html, foto, history FROM peoples WHERE (age > 33 OR age = 0) AND ' \
                  't_link >= %s AND t_link <= %s AND t_people >= %s  AND t_people <= %s AND mamba_id = %s ' + sql_append
            read_cursor.execute(sql, (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo,
                                      s(self.leFilter.text())))
        else:
            sql = 'SELECT DATE_FORMAT(access_date,"%d.%m %H:%i"), her_name, age, msg, fotos_count, id, msg_id, mamba_id, ' \
                  't_people, t_link, html, foto, history FROM peoples WHERE (age > 33 OR age = 0) AND ' \
                  't_link >= %s AND t_link <= %s AND t_people >= %s AND t_people <= %s ' + sql_append
            read_cursor.execute(sql, (self.stLinkFrom, self.stLinkTo, self.stPeopleFrom, self.stPeopleTo))

        rows = read_cursor.fetchall()
        self.tableWidget.setColumnCount(3)             # Устанавливаем кол-во колонок
        self.tableWidget.setRowCount(len(rows))        # Кол-во строк из таблицы
        self.id_all = []
        self.histories = {}
        self.foto = {}
        self.html = {}
        self.t_link = {}
        self.t_people = {}
        self.mamba_id = {}
        self.msg_id = {}
        i = 0
        for row in rows:
            html_tek = row[len(row)-3]
            self.scan(html_tek)
            show = True
            if self.chb_mar.isChecked():
                if not self.chk_marr:
                    show = False
            if self.chb_baryg.isChecked():
                if not self.chk_baryg:
                    show = False
            if self.chb_child.isChecked():
                if not self.chk_child:
                    show = False
            if self.chb_dist.isChecked():
                if not self.chk_dist:
                    show = False
            if self.chb_edu.isChecked():
                if not self.chk_educ:
                    show = False
            if self.chb_home.isChecked():
                if not self.chk_home:
                    show = False
            if not show:
                continue
            self.id_all.append(int(row[len(row)-8]))
            self.id_tek = int(row[len(row)-8])
            for j, cell in enumerate(row):
                if j == len(row) - 8:
                    q = 0
                elif j == len(row) - 1:
                    self.histories[self.id_tek] = cell
                elif j == len(row) - 2:
                    self.foto[self.id_tek] = cell
                elif j == len(row) - 3:
                    self.html[self.id_tek] = cell
                    self.scan(cell)
                elif j == len(row) - 4:
                    self.t_link[self.id_tek] = cell
                elif j == len(row) - 5:
                    self.t_people[self.id_tek] = cell
                elif j == len(row) - 6:
                    self.mamba_id[self.id_tek] = cell
                elif j == len(row) - 7:
                    self.msg_id[self.id_tek] = cell
                elif j == len(row) - 9:                        # Количество загруженных фоток
                    self.fotos_count[self.id_tek] = cell
                elif j == len(row) - 10:
                    q = 0                                     # сообщения не показывает, с...
                elif j == len(row) - 11:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(cell)))
                    self.ages[self.id_tek] = str(cell)
                elif j == len(row) - 12:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(cell)))
                    self.names[self.id_tek] = str(cell)
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(cell)))
            i += 1
        self.tableWidget.setRowCount(len(self.id_all))        # Обрезаем кол-во строк с учетом фильтров

        if len(self.id_all) > 0:
            self.id_tek = self.id_all[0]
#        self.mamba_id_tek = self.mamba_id[self.id_tek]
#        self.msg_id_tek = self.msg_id[self.id_tek]
        # Устанавливаем заголовки таблицы
        self.tableWidget.setHorizontalHeaderLabels(["Активность", "Имя", "Возраст"])

        # Устанавливаем выравнивание на заголовки
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableWidget.resizeColumnsToContents()
        self.click_tableWidget()
        return

    def click_tableWidget(self, index=None):
        if index == None:
            index = self.tableWidget.model().index(0, 0)
        else:
            self.updateHistory()
        if index.row() < 0:
            return None
        self.id_tek = self.id_all[index.row()]
        self.textEdit.setText(self.histories[self.id_tek])
        self.cbLink.setCurrentIndex(self.t_link[self.id_tek])
        self.cbPeople.setCurrentIndex(self.t_people[self.id_tek])
        pixmap = QPixmap()
        pixmap.loadFromData(self.foto[self.id_tek],'JPG')
        self.label_3.setPixmap(pixmap)
        self.anketa_html.setHtml(self.html[self.id_tek])
#        try:
#            self.chb_baryg.setChecked(self.chk_baryg[self.id_tek])
#            self.chb_child.setChecked(self.chk_child[self.id_tek])
#            self.chb_dist.setChecked(self.chk_dist[self.id_tek])
#            self.chb_edu.setChecked(self.chk_educ[self.id_tek])
#            self.chb_home.setChecked(self.chk_home[self.id_tek])
#            self.chb_mar.setChecked(self.chk_marr[self.id_tek])
#        except:
#            a = crop_tags(self.html[self.id_tek])

        self.setup_tableFotos()
        if self.msg_id[self.id_tek] == None:
            self.pbToMessage.setEnabled(False)
        else:
            self.pbToMessage.setEnabled(True)
        return None

    def click_cbLink(self):
        self.dbconn.connect()
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
        return

    def setup_tableFotos(self):
        mamba_id = self.mamba_id[self.id_tek]
        name = self.names[self.id_tek]
        count = self.fotos_count[self.id_tek]
        self.tableFotos.setColumnCount(0)
        self.tableFotos.setRowCount(1)
        self.tableFotos.setColumnCount(count)
        for i in range(1, count + 1):
            self.tableFotos.setItem(0, i-1, QTableWidgetItem(str(i)))
        self.tableFotos.resizeColumnsToContents()

    def click_label_3(self, index=None):
        if index == None or index.row() < 0 or index.row() > 0 or index.column() < 0:
            index = self.tableFotos.model().index(0, 0)
        pixmap = QPixmap('photos/'+ self.mamba_id[self.id_tek] + '_' + s(self.names[self.id_tek]).replace(' ','') +
                         s(self.ages[self.id_tek]) + '_' + '{0:02d}'.format(index.column()+1) + '.jpg')
        self.label_3.setPixmap(pixmap)

    def click_tableFotos(self, index=None):
        if index == None or index.row() < 0 or index.row() > 0 or index.column() < 0:
            index = self.tableFotos.model().index(0, 0)
        proc = Popen('nomacs ' + 'photos/'+ self.mamba_id[self.id_tek] + '_' + s(self.names[self.id_tek]).replace(' ','') +
                     s(self.ages[self.id_tek]) + '_' + '{0:02d}'.format(index.column()+1) + '.jpg', shell=True,
                     stdout=PIPE, stderr=PIPE)
        proc.wait()  # дождаться выполнения
        res = proc.communicate()  # получить tuple('stdout', 'stderr')
        if proc.returncode:
            print(res[1])
            print('result:', res[0])

    def click_cbPeople(self):
        self.dbconn.connect()
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
        return

    def click_cbLinkFrom(self):
        self.stLinkFrom = self.cbLinkFrom.currentIndex()
        self.setup_tableWidget()
        return

    def click_cbLinkTo(self):
        self.stLinkTo = self.cbLinkTo.currentIndex()
        self.setup_tableWidget()
        return

    def click_cbStatus(self):
        self.stStatus = self.cbStatus.currentIndex()
        self.setup_tableWidget()
        return

    def click_cbPeopleFrom(self):
        self.stPeopleFrom = self.cbPeopleFrom.currentIndex()
        self.setup_tableWidget()
        return

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
            self.dbconn.connect()
            write_cursor = self.dbconn.cursor()
            write_cursor.execute('UPDATE peoples SET history = %s WHERE id = %s', (current, self.id_tek))
            self.dbconn.commit()
            self.histories[self.id_tek] = current
        return

    def convert_mamba_id(self, href):
        a = "".join([k.strip() for k in href]).strip()
        m_id = a[21:].split("?")[0]
        if len(m_id.split('#')) > 1:
            m_id = m_id.split('#')[0]
        if len(m_id.split('&')) > 1:
            m_id = m_id.split('&')[0]
#        print(a, a[21:], m_id)
        return m_id

    def convert_msg_id(self, m_id):
        if m_id[:2] == 'mb':
            return m_id[2:]
        else:
            return None

    def scan(self, html_tek):
        a = crop_tags(html_tek)
        self.chk_educ = False
        self.chk_child = False
        self.chk_home = False
        self.chk_baryg = False
        self.chk_marr = False
        self.chk_dist = False
        if a.find('Образование: среднее') == -1 and a.find('Образование: среднее специальное') == -1 \
                and a.find('Образование: неполное высшее') == -1:
            self.chk_educ = True
        if a.find('Дети: Есть, живём вместе') == -1:
            self.chk_child = True
        if a.find('Проживание: Комната в общежитии, коммуналка') == -1 and \
                        a.find('Проживание: Живу с родителями') == -1 and \
                        a.find('Проживание: Живу с приятелем / с подругой') == -1 and \
                        a.find('Проживание: Нет постоянного жилья') == -1:
            self.chk_home = True
        if a.find('Материальная поддержка: Ищу спонсора') == -1:
            self.chk_baryg = True
        if a.find('Отношения: В браке') == -1 and a.find('Отношения: Есть отношения') == -1:
            self.chk_marr = True
        if a.find('~') > -1:
            if a.find(' км ') > -1:
                dist = int(a[a.find('~') + 1:a.find('км')])
            else:
                dist = 0
            if dist < 20:
                self.chk_dist = True
        else:
            self.chk_dist = True
        return

    def click_pbScan(self):
        if self.refresh_started:
            return
        for id_curr in self.id_all:
            if self.fotos_count[id_curr] == 0:                               # !!!!! Временно !!!!!
                aa = 'https://www.mamba.ru/' + self.mamba_id[id_curr]
                self.drv.get(url=aa)
                wj(self.drv)
                self.click_pbGetHTML()
        return


    def deep_old_scan(self):        # старое глубокое сканирование
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
                self.dbconn.connect()
                read_cursor = self.dbconn.cursor()
                read_cursor.execute('SELECT id, html FROM peoples WHERE mamba_id = %s', (mamba_id,))
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
                    html_locator = p(d=self.drv, f='p', **B['anketa-locator'])
                    html_abouts = p(d=self.drv, f='ps', **B['anketa-about'])
                    html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/' \
                           'strict.dtd"><html><head></head><body><p>' + html_msg + '</p><h3>' + html_locator + '</h3><p>'
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
                    self.html[row_ch[0][0]] = html
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
        return


    def click_pbReLogin(self):
        self.drv.quit()
        self.drv = webdriver.Firefox()  # Инициализация драйвера
        self.drv.implicitly_wait(5)  # Неявное ожидание - ждать ответа на каждый запрос до 5 сек
        authorize(self.drv, **self.webconfig)  # Авторизация
        self.refresh_started = False               # Выключаем автообновление
        self.pbRefresh.setText('Обновить')
        wj(self.drv)
        return


    def click_pbRefresh(self):                     # Включение автообновления
        if self.refresh_started == False:
            if len(self.drv.window_handles) < 2:
                self.drv.execute_script('''window.open("about:blank", "_blank");''')
                self.drv.switch_to.window(self.drv.window_handles[1])
                self.drv.get(**self.messages)  # Открытие страницы где сообщения
                self.drv.switch_to.window(self.drv.window_handles[0])
            self.refresh_started = True
            self.pbRefresh.setText('ОБНОВЛЯЮ')
            self.myTimer.stop()
            self.myTimer.start(300000)
        else:
            self.refresh_started = False
            self.pbRefresh.setText('Обновить')
        wj(self.drv)

    def refreshing(self):                           # Обновление статусов
        if not self.refresh_started:
            return
        self.myTimer.stop()
        self.drv.switch_to.window(self.drv.window_handles[0])
        sql = 'UPDATE peoples SET status = 0 WHERE status != 0'     # Сначала всех в оффлайн
        self.dbconn.connect()
        write_cursor = self.dbconn.cursor()
        write_cursor.execute(sql)
        self.dbconn.commit()
        self.drv.get(**self.fillconfig)  # Открытие страницы где поиск
        page = 0
#        standart = len(p(d=self.drv, f='ps', **B['tiles']))
        i_tek = 0
        outs = []
        updates = []
        statuses = []
        has_new = True
        loaded_mamba_ids = []
        while has_new:
#            page_link = self.drv.find_element_by_xpath('//DIV[@class="pager wrap"]//LI[text()="' + str(page) + '"]')
#            page_link.click()
            self.drv.execute_script("window.scrollTo(0, " + str(page*3000) + ");")
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
            has_new = False
            reload = False
            q = len(tiles)
            if len(names) != q or len(hrefs) != q or len(fotos_hrefs) != q:
                print('Обновление: Количество в массивах не совпадает')
                break
#            tiles[0].location_once_scrolled_into_view
            for i, mamba_href in enumerate(hrefs):
                nextload = False
                mamba_id = self.convert_mamba_id(mamba_href)
                for loaded_mamba_id in loaded_mamba_ids:
                    if loaded_mamba_id == mamba_id:
                        nextload = True
                if nextload:
                    continue
                has_new = True
                row_ch = []
                read_cursor = self.dbconn.cursor()
                read_cursor.execute('SELECT id, html FROM peoples WHERE mamba_id = %s',(mamba_id,))
                row_ch = read_cursor.fetchall()
                if len(row_ch) < 1: # карточки (записи в БД) нет
                    out = tuple()
                    html = None
                    age = 0
                    if len(names[i].split(',')) > 1:
                        age = l(names[i].split(',')[1].strip())
                    out += (mamba_id, ) + (self.convert_msg_id(mamba_id), ) + (names[i].split(',')[0].strip(), ) + (age,)
                    status = 0
                    try:
                        foto = urllib.request.urlopen(fotos_hrefs[i], timeout=10).read()
                    except:
                        foto = BREAKED_MAMBA
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                            statuses.append((status, foto, mamba_id))
                    try:
                        tiles[i].click()
                    except:
                        q = 0
                    else:
                        try:
                            wj(self.drv)
                            html = self.get_html()
                            back = p(d=self.drv, f='c', **B['back-find'])
                            wj(self.drv)
                            back.click()
                            wj(self.drv)
                        except:
                            q = 0
                    out += (status, ) + (foto, ) + (html, )
                    outs.append(out)
#                    i_tek += 1
                    reload = True
                elif not row_ch[0][1]:  # html нет а карточка (запись в БД) есть
                    update = tuple()
                    html = None
                    try:
                        foto = urllib.request.urlopen(fotos_hrefs[i], timeout=10).read()
                    except:
                        foto = BREAKED_MAMBA
                    status = 0
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                            statuses.append((status, foto, mamba_id))
                    try:
                        tiles[i].click()
                    except:
                        q = 0
                    else:
                        try:
                            wj(self.drv)
                            html = self.get_html()
                            try:
                                foto = urllib.request.urlopen(fotos_hrefs[i], timeout=10).read()
                            except:
                                foto = BREAKED_MAMBA
                            back = p(d=self.drv, f='c', **B['back-find'])
                            wj(self.drv)
                            back.click()
                            wj(self.drv)
                        except:
                            q = 0
                    update += (html,) + (status,) + (foto, ) + (row_ch[0][0],)
#                    update += (status,) + (row_ch[0][0],)
                    updates.append(update)
                    reload = True
#                    i_tek += 1
                else:                   # есть и html и карточка
                    status = 0
                    try:

                        foto = urllib.request.urlopen(fotos_hrefs[i], timeout=10).read()
                    except:
                        foto = BREAKED_MAMBA
                    for status_href in hrefs_onln:
                        if self.convert_mamba_id(status_href) == mamba_id:
                            status = 1
                            statuses.append((status, foto, mamba_id))
                loaded_mamba_ids.append(mamba_id)
                if reload:
                    break
            if len(outs) > 0:
                sql = 'INSERT INTO peoples(mamba_id, msg_id, her_name, age, status, foto, html) ' \
                      'VALUES (%s,%s,%s,%s,%s,%s,%s)'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, outs)
                self.dbconn.commit()
            if len(updates) > 0:
                sql = 'UPDATE peoples set html = %s, status = %s, foto = %s WHERE id = %s'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, updates)
                self.dbconn.commit()
            if len(statuses) > 0:
                sql = 'UPDATE peoples SET status = %s, foto = %s, access_date = NOW() WHERE mamba_id = %s'
                write_cursor = self.dbconn.cursor()
                write_cursor.executemany(sql, statuses)
                self.dbconn.commit()
            else:                              # Если нет ни одного в онлайне - выходим
                self.setup_tableWidget()
                self.myTimer.start(300000)
                return
            outs = []
            updates = []
            statuses = []
            if (not reload) or (i == len(hrefs)-1):
#                self.drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.drv.execute_script("window.scrollTo(0, 3000);")
                page += 1

#            if i_tek >= len(hrefs) - 1:
#                page += 1
#                i_tek = 0
            q=0
        q = 0
        self.setup_tableWidget()
        self.myTimer.start(300000)
        return

    def click_pbToAnketa(self):
        if self.refresh_started:
            self.drv.switch_to.window(self.drv.window_handles[1])
        aa = 'https://www.mamba.ru/' + self.mamba_id[self.id_tek]
        self.drv.get(url=aa)
        wj(self.drv)
        self.click_pbGetHTML()
        return

    def click_pbToMessage(self):
        if self.refresh_started:
            self.drv.switch_to.window(self.drv.window_handles[1])
        aa = 'https://www.mamba.ru/my/message.phtml?uid=' + self.msg_id[self.id_tek]
        self.drv.get(url=aa)
        return

    def get_html(self):
        html_msg = p(d=self.drv, f='p', **B['anketa-msg'])
        html_favour = p(d=self.drv, f='p', **B['anketa-favour'])
        html_abouts = p(d=self.drv, f='ps', **B['anketa-about'])
        html_locator = p(d=self.drv, f='p', **B['anketa-locator'])
        html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/' \
               'strict.dtd"><html><head></head><body><p>' + html_msg + '</p><h3>' + html_locator + '</h3><p>'
        html += html_favour.replace('\n', ' | ') + '</p>'
        if len(html_abouts) > 0:
            for html_into in html_abouts:
                html += html_into
        html = html.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('  ', ' ')
        html = html.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        html = html.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        html += '</body></html>'
        return html

    def click_pbGetHTML(self):
        if self.refresh_started:
            self.drv.switch_to.window(self.drv.window_handles[1])
        mamba_id_there = self.convert_mamba_id(self.drv.current_url)
        if len(mamba_id_there.split('#')) > 1:
            mamba_id_there = mamba_id_there.split('#')[0]
        if len(mamba_id_there.split('&')) > 1:
            mamba_id_there = mamba_id_there.split('&')[0]
        if len(mamba_id_there.split('?')) > 1:
            mamba_id_there = mamba_id_there.split('?')[0]
        self.dbconn.connect()
        read_cursor = self.dbconn.cursor()
        read_cursor.execute('SELECT id, her_name, age FROM peoples WHERE mamba_id = %s', (mamba_id_there,))
        row_row = read_cursor.fetchall()
        if len(row_row) > 0:
            id_there = row_row[0][0]
            anketa_deleted = p(d=self.drv, f='p', **B['anketa-deleted'])
            if anketa_deleted != None:
                sql = 'UPDATE peoples SET t_link = 0 WHERE mamba_id = %s'
                write_cursor = self.dbconn.cursor()
                write_cursor.execute(sql, (mamba_id_there,))
                self.dbconn.commit()
                return
            her_name = row_row[0][1]
            age = row_row[0][2]
            wj(self.drv)
            no_fotos = p(d=self.drv, f='p', **B['no-fotos'])
            wj(self.drv)
            if no_fotos == None:
                open_fotos = p(d=self.drv, f='c', **B['open-fotos'])
                wj(self.drv)
                open_fotos.click()
                time.sleep(1)
                all_fotos = p(d=self.drv, f='ps', **B['all-fotos'])
                wj(self.drv)
                if all_fotos != None:                           # Грузим все фотки
                    if len(all_fotos) > self.fotos_count[id_there] :
                        for i, all_foto in enumerate(all_fotos):
                            if all_foto.is_displayed():
                                all_foto.click()
                            wj(self.drv)
                            big_foto = p(d=self.drv, f='p', **B['big-foto'])
                            try:
                                foto = urllib.request.urlopen(big_foto, timeout=10).read()
                            except:
                                foto = BREAKED_MAMBA
                            f = open('./photos/'+ mamba_id_there + '_' + s(her_name).replace(' ','').replace('\n','')
                                     + s(age) + '_' + '{0:02d}'.format(i+1) + '.jpg', 'wb')
                            f.write(foto)
                            f.close()
                        self.fotos_count[id_there] = len(all_fotos)
                else:
                    if 1 > self.fotos_count[id_there]:
                        big_foto = p(d=self.drv, f='p', **B['big-foto'])
                        try:
                            foto = urllib.request.urlopen(big_foto, timeout=10).read()
                        except:
                            foto = BREAKED_MAMBA
                        f = open('./fotos/' + mamba_id_there + '_' + s(her_name).replace(' ','') + s(age) + '_01' +
                                 '.jpg', 'wb')
                        f.write(foto)
                        f.close()
                    self.fotos_count[id_there] = 1
                close_fotos = p(d=self.drv, f='ps', **B['close-fotos'])
                wj(self.drv)
                close_fotos[0].click()
            wj(self.drv)
            html_msg = p(d=self.drv, f='p', **B['anketa-msg'])
            html_favour = p(d=self.drv, f='p', **B['anketa-favour'])
            html_abouts = p(d=self.drv, f='ps', **B['anketa-about'])
            html_locator = p(d=self.drv, f='p', **B['anketa-locator'])
            html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/' \
                   'strict.dtd"><html><head></head><body><p>' + html_msg + '</p><h3>' + html_locator + '</h3><p>'
            html += html_favour.replace('\n', ' | ') + '</p>'
            if len(html_abouts) > 0:
                for html_into in html_abouts:
                    html += html_into
            html = html.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('  ', ' ')
            html = html.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
            html = html.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
            html += '</body></html>'
            self.html[id_there] = html
            self.anketa_html.setHtml(html)
            sql = 'UPDATE peoples SET html = %s, fotos_count = %s WHERE mamba_id = %s'
            write_cursor = self.dbconn.cursor()
            write_cursor.execute(sql, (html, self.fotos_count[id_there], mamba_id_there))
            self.dbconn.commit()
            read_cursor = self.dbconn.cursor()
            read_cursor.execute('SELECT msg_id FROM peoples WHERE mamba_id = %s', (mamba_id_there,))
            row_msg = read_cursor.fetchall()
            if len(row_msg) > 0:
                if row_msg[0][0] == None:
                    sql = 'UPDATE peoples SET msg_id = %s WHERE mamba_id = %s'
                    write_cursor = self.dbconn.cursor()
                    aa = p(d=self.drv, f='p', **B['anketa-btn'])
                    ab = aa.split('uid=')[1]
                    write_cursor.execute(sql, (ab, mamba_id_there))
                    self.dbconn.commit()
                    self.msg_id[mamba_id_there] = ab
            wj(self.drv)
        return


