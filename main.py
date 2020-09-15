# main.py

import sys
import python_websocket_client
from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QTextEdit
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import *
from PySide2.QtCore import *
import json


class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(640, 480)
        # 1 - create Worker and Thread inside the Form
        self.obj = python_websocket_client.Worker()  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        # self.obj.start.connect(self.onStart)
        # self.obj.stop.connect(self.onStop)
        # self.obj.message.connect(self.onMessage)
        self.obj.message.connect(self.onMessage)
        self.obj.data.connect(self.onData)

        # 3 - Move the Worker object to the Thread object
        self.obj.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        # self.obj.stop.connect(self.obj.stopclient)
        # self.obj.start.connect(self.obj.startclient)

        # 5 - Connect Thread started signal to Worker operational slot method
        # self.thread.started.connect(self.obj.startclient)

        # * - Thread finished signal will close the app if you want!
        # self.thread.stop.connect(self.obj.stopclient)

        # 6 - Start the thread
        self.thread.start()

        # 7 - Start the form
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.startbutton = QPushButton("start")
        self.info = QTextEdit(self)
        # self.info.append('Hello')
        grid.addWidget(self.info)
        grid.addWidget(self.startbutton)
        self.stopbutton = QPushButton("stop")
        grid.addWidget(self.stopbutton)

        self.move(300, 150)
        self.setWindowTitle('thread test')
        self.show()

        self.startbutton.clicked.connect(self.start)
        self.stopbutton.clicked.connect(self.stop)

    def start(self):
        self.obj.startclient()

    def stop(self):
        self.obj.stopclient()

    def onMessage(self, msg):
        self.info.append(msg)

    def onData(self, data):
        jsonData = json.dumps(data, indent=4, sort_keys=True)
        self.info.append(jsonData)

    def onStop(self, msg):
        self.info.append('I am Diconnected')

    # def onConnected(self, msg):
    #     self.info.append('I am connected')

    # Create the Qt Application


#
app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())

# Create and show the form
# form = Form()
# form.show()
