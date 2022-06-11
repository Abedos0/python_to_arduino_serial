
import serial
import time

from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit,QLabel, QPushButton, QApplication, QGridLayout

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ser = serial.Serial(baudrate=115200, timeout=0.5, port='COM4')
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.text_field = QPlainTextEdit("")
        self.grid.addWidget(self.text_field, 1, 0)
        self.text_field.setMinimumSize(600, 200)

        self.save_button = QPushButton("Save to arduino")
        self.save_button.clicked.connect(self.button_clicked)
        self.grid.addWidget(self.save_button, 2, 0)

        self.read_prog_button = QPushButton("Read program")
        self.read_prog_button.clicked.connect(self.read_prog_clicked)
        self.grid.addWidget(self.read_prog_button, 3, 0)

        self.read_states_button = QPushButton("Read states")
        self.read_states_button.clicked.connect(self.read_states_clicked)
        self.grid.addWidget(self.read_states_button, 4, 0)

        self.label = QLabel('hello\nDUDE')
        #self.label.setPixmap(QPixmap(QImage('py_image.jpg')))
        # self.label.setWindowIcon(QIcon('py_image.jpg'))
        self.grid.addWidget(self.label, 0, 0)

    def __del__(self):
        self.ser.close()

    def button_clicked(self):
        self.ser.write(b">WRITE_PROG@\n")

        commands = self.text_field.toPlainText().replace('\r', '')
        print(f'Commands len = {len(commands)}')
        commands = commands.split('\n')
        for command in commands:
            cmd_bytes = bytes(command, 'ascii')
            print(cmd_bytes)
            self.ser.write(cmd_bytes+b'\n')
            time.sleep(0.01)

        self.ser.write(b"ENDCOM#\n")

        time.sleep(0.2)
        data = self.ser.readall()
        print(data.decode('utf-8'))

    def read_prog_clicked(self):
        command = bytes(">READ_PROG@", 'ascii')
        self.ser.write(command)
        time.sleep(0.1)
        data = self.ser.readall()
        print(data.decode('utf-8'))

    def read_states_clicked(self):
        command = bytes(">GET_STATES@", 'ascii')
        self.ser.write(command)
        time.sleep(0.1)
        data = self.ser.readall()
        print(data.decode('utf-8'))

# 1. connect self.save_button click event to button_clicked method
# 2. take command from text field
# 3. Add Qlabel
# 4. Resize window.


app = QApplication([])
window = QMainWindow()
window.setWindowIcon(QIcon('py_image.jpg'))
widg = MainWidget()
window.setCentralWidget(widg)
window.show()
app.exec_()

