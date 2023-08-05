import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import re


from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))

from . import server as server
from . import users_list as users_list
# from .server import gui_server import server, users_list
#

# from ..jim.settings import *
from jim.settings import *

# IP_SERVER_DEFAULT, PORT_SERVER_DEFAULT
# QT_DEBUG_PLUGINS=1


class MySetWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pattern = re.compile(PATTERN_IP)

        self.ui = server.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setText(IP_SERVER_DEFAULT)
        self.ui.lineEdit_2.setText(str(PORT_SERVER_DEFAULT))

        self.ui.pushButton.clicked.connect(self.save_settings)

        print('self.pattern', self.pattern)

    def save_settings(self):
        self.ip = self.ui.lineEdit.text()
        self.port = self.ui.lineEdit_2.text()
        if self.verification_address():
            print(self.ip, ' - ', self.port)
            self.close()
            # sys.exit(app.exec_())

    def verification_address(self):
        flag = True
        if re.match(self.pattern, self.ip) or self.ip == '':
            print('TRUE')
            self.ui.lineEdit.setStyleSheet("QLineEdit {background-color:rgba(255, 255, 255, 255)}")
        else:
            print('ELSE')
            self.ui.lineEdit.setStyleSheet("QLineEdit {background-color:rgba(255, 0, 0, 150)}")
            self.ip = IP_SERVER_DEFAULT
            flag = False

        try:
            self.port = int(self.port)
            if self.port < 1023 or self.port > 65536:
                raise ValueError('Число вне диапазона: 1023-65536')
        except ValueError:
            self.ui.lineEdit_2.setStyleSheet("QLineEdit {background-color:rgba(255, 0, 0, 150)}")
            flag = False
        else:
            self.ui.lineEdit_2.setStyleSheet("QLineEdit {background-color:rgba(255, 255, 255, 255)}")

        return flag


class UsersListWin(QtWidgets.QMainWindow):
    def __init__(self, s, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.s = s
        self.ui = users_list.Ui_MainWindow()
        self.ui.setupUi(self)
        # server = ServerDataBase()

        # server.log_in('Yana', 'qwerty1', '127.0.0.124')
        # server.log_in('Oleg', 'qwerty2', '127.0.0.14')
        # server.log_in('Lily', 'qwerty3', '127.0.0.24')
        # server.log_in('Elena', 'qwerty3', '127.0.0.26')

        users = self.s.get_users_list()
        self.ui.tableWidget.setRowCount(len(users))
        row = 0
        for item in users:
            id = QtWidgets.QTableWidgetItem(str(item.id))
            login = QtWidgets.QTableWidgetItem(item.login)
            info = QtWidgets.QTableWidgetItem(item.information)

            self.ui.tableWidget.setItem(row, 0, id)
            self.ui.tableWidget.setItem(row, 1, login)
            self.ui.tableWidget.setItem(row, 2, info)
            row += 1
        self.ui.tableWidget.resizeColumnsToContents()

        # Create new action
        setAction = QtWidgets.QAction(QtGui.QIcon('images.png'), '&Settings', self)
        setAction.setShortcut('Ctrl+Alt+S')
        setAction.setStatusTip('Settings')
        setAction.triggered.connect(self.start_settings)

        # # Create new action
        # openAction = QtWidgets.QAction(QtGui.QIcon('images.png'), '&Open', self)
        # openAction.setShortcut('Ctrl+O')
        # openAction.setStatusTip('Open document')
        # # openAction.triggered.connect( self.ui.openCall)
        #
        # # Create exit action
        # exitAction = QtWidgets.QAction(QtGui.QIcon('images.png'), '&Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # # exitAction.triggered.connect( self.ui.exitCall)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('& File')

        fileMenu.addAction(setAction)
        # fileMenu.addAction(openAction)
        # fileMenu.addAction(exitAction)

    def start_settings(self):
        self.set_app = MySetWin()
        self.set_app.setWindowTitle('Settings')
        self.set_app.show()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # set_app = MySetWin()
    # set_app.setWindowTitle('Settings')
    # set_app.show()

    users_list_app = UsersListWin()
    users_list_app.setWindowTitle('Users list')
    users_list_app.show()


    sys.exit(app.exec_())

# pyuic5 project/gui_server/server.ui -o project/gui_server/server.py
