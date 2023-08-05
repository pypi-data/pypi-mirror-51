from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from gui_server.main import *
import server as logic_servers


s = logic_servers.Server()
s.start_server()
