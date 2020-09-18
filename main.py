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
        hand_string = self.convertdata(data)
        self.info.append(hand_string)

    def onStop(self, msg):
        self.info.append('I am Diconnected')

    # def onConnected(self, msg):
    #     self.info.append('I am connected')

    # Create the Qt Application

    def convertdata(self, data):
        # mocap data order
        # thumb: [0, 1, 2, 3, 4],
        # indexFinger: [0, 5, 6, 7, 8],
        # middleFinger: [0, 9, 10, 11, 12],
        # ringFinger: [0, 13, 14, 15, 16],
        # pinky: [0, 17, 18, 19, 20],
        # hand_data = json.dumps(data, indent=4, sort_keys=True)

        beg = "0, 105, 0, 0, 0, 0, \
              -11, 105, 0, 0, 0, 0, \
              -11, 56, 0, 0, 0, 0, \
              -11, 8, 0, 0, 0, 0, \
              11, 105, 0, 0, 0, 0, \
              11, 56, 0, 0, 0, 0, \
              11, 8, 0, 0, 0, 0.0, \
              0, 118, 0, 0, 0, 0, \
              0, 129, 0, 0, 0, 0, \
              0, 141, 0, 0, 0, 0, \
              0, 152, 0, 0, 0, 0, \
              0, 164, 0, 0, 0, 0, \
              0, 173, 0, 0, 0, 0, \
              -3, 160, 0, 0, 0, 0, \
              -17, 160, 0, 0, 0, 0,"

        # Generated data will be inserted between beg and end
        end = "3, 160, 0, 0, 0, 0, \
              17, 160, 0, 0, 0, 0, \
              46, 160, 0, 0, 0, 0, \
              74, 160, 0, 0, 0, 0, \
              77, 161, 3, 0, -30, 0, \
              81, 161, 3, 0, 0, 0, \
              83, 161, 3, 0, 0, 0, \
              78, 161, 2, 0, 0, 0, \
              83, 161, 3, 0, 0, 0, \
              87, 161, 3, 0, 0, 0, \
              89, 161, 3, 0, 0, 0, \
              78, 161, 0, 0, 0, 0, \
              83, 161, 1, 0, 0, 0, \
              88, 161, 1, 0, 0, 0, \
              90, 161, 1, 0, 0, 0, \
              78, 161, 0, 0, 0, 0, \
              83, 161, 0, 0, 0, 0, \
              86, 161, 0, 0, 0, 0, \
              89, 161, 0, 0, 0, 0, \
              77, 161, -1, 0, 0, 0, \
              82, 161, -2, 0, 0, 0, \
              85, 161, -2, 0, 0, 0, \
              87, 161, -2, 0, 0, 0"

        palm_position = data[0]['points'][0]  # palm position
        rotationstring = "0.0,0,0,"
        hand_str = ""
        joint_string = ""
        for fingerdictionary in data:
            finger = fingerdictionary['finger']
            joint = fingerdictionary['points']
            if finger == "thumb":
                del joint[0]  # Remove palm point
                del joint[0]  # Remove palm point two
            else:
                del joint[0]  # Remove palm point

            for coordinates in joint:
                x = "{:.2f}".format(coordinates[0])
                y = "{:.2f}".format(coordinates[1])
                z = "{:.2f}".format(coordinates[2])
                joint_string = str(x) + "," + str(y) + "," + str(z) + "," + str(rotationstring)

            hand_str += joint_string

        hand_string = "[" + beg + hand_str + end + "]"
        return hand_string
    # hand_str = hand_str[:-1] remove last comment


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())

# Create and show the form
# form = Form()
# form.show()
