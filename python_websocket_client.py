# python -m pip install "python-socketio[client]" #
# python -m pip install "Pyside2" #
from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, Slot
import socketio

sio = socketio.Client()
url = 'ws://localhost:5000'
transport = 'websocket'
myroom = "pythonclient"


class Worker(QtCore.QObject):
    stop = Signal(str)
    message = Signal(str)
    data = Signal(dict)

    def __init__(self):
        super().__init__()  # This is required!
        # Other initialization...

        # self.intReady.connect(self.print_msg)

    @Slot()
    def startclient(self):
        if sio.sid:
            self.message.emit("Already connected")
        else:
            self.message.emit('I am starting')
            sio.connect(url, transports=transport)

            @sio.on('connect')
            def connect():
                self.message.emit("I am connecting")
                sio.emit('Connected id  ', sio.sid)
                sio.emit('room', myroom)
                self.message.emit("Joined room  " + myroom)

            @sio.on('message')
            def message(string):
                self.message.emit(string)

            @sio.on('data')
            def data(dictionary):
                self.data.emit(dictionary)

            @sio.on('connect_error')
            def connect_error():
                self.message.emit("Connection failed!")

            @sio.on('disconnect')
            def disconnect():
                self.message.emit("Disconnected!")
                sio.disconnect()

    def stopclient(self):
        self.message.emit('I am stopping')
        sio.disconnect()
