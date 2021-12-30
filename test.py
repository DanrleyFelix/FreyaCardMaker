import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QSlider, QPushButton, 
QMainWindow, QAction, qApp,
    QLCDNumber, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, 
QSizePolicy, QScrollArea, QLayout)
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QRect


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setWindowTitle("My Awesome App")
        size = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        layout = QVBoxLayout()
        layout2 = QVBoxLayout()
        brw = Color2('brown')
        brw.setSizePolicy(size)
        layout2.addWidget(brw)
        layout2.addWidget(Color('black'))
        layout2.setStretch(1,2)
        layout2.addWidget(Color('cyan'))
        layout2.setStretch(2, 1)

        layout.addWidget(Color('red'))
        layout.addWidget(Color('blue'))
        layout.addWidget(Color('green'))

        self.scrollArea = QScrollArea()
        # set CentralWidget
        self.setCentralWidget(self.scrollArea)

        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 600, 500))   
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setMinimumSize(QSize(500, 500))

        self.scrollLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        #self.scrollLayout.setSizeConstraint(QLayout.SetMinimumSize) #2
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(Color('purple'))
        self.mainLayout.addWidget(Color('yellow'))
        self.mainLayout.addWidget(Color('orange'))
        self.mainLayout.addLayout(layout2)
        self.mainLayout.addLayout(layout)
        self.scrollLayout.addLayout(self.mainLayout)

        self.show()

app = QApplication(sys.argv)
#print(QDesktopWidget().availableGeometry())

window = Window()
sys.exit(app.exec_())