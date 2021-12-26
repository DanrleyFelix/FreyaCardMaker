import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from utils import *
from style import *
from json_manager import JsonManager
from os.path import basename


jmanager = JsonManager()


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.top = 100
        self.left = 100
        self.width = 1080
        self.height = 800
        self.title = "Freya Card Maker"
        stylesheet = ""
        self.dialogUploadIsFromWeb = False
        self.lastEditionJson = jmanager.readJson('presets//last_edition.json')
        self.dirJson = jmanager.readJson('data//data.json')
        self.imageDir = ''
        self.imageFormats = ['.png','.gif','.jpeg']
        self.box_list = []
        self.imgPreset = 'interface//temp.gif'
        with open("design.qss", "r") as f:
            stylesheet = f.read()
        self.interface = QLabel(self)
        interface_backgropund = QtGui.QPixmap('interface//background.png')
        self.interface.setPixmap(interface_backgropund)
        self.interface.resize(1080,800)
        label_img = QLabel(self)
        label_img.move(700,100)
        label_img.resize(370,520)
        self.movie = QtGui.QMovie(self.imgPreset)
        label_img.setMovie(self.movie)
        self.movie.start()
        ld = label_distance(100,800,70)
        self.create_label([50,ld[0]],'interface_font',[100,30],'Name:')
        self.create_label([50,ld[1]],'interface_font',[125,30],'Attribute:')
        self.create_label([50,ld[2]],'interface_font',[200,30],'Race/Class:')
        self.create_label([50,ld[3]],'interface_font',[125,30],'Rating:')
        self.create_label([50,ld[4]],'interface_font',[100,30],'Rank:')
        self.create_label([50,ld[5]],'interface_font',[110,30],'Image:')
        self.create_label([50,ld[6]],'interface_font',[165,30],'Background:')
        self.create_label([50,ld[7]],'interface_font',[100,30],'MP:')
        self.create_label([50,ld[8]],'interface_font',[165,30],'Card Points:')
        self.create_label([50,ld[9]],'interface_font',[100,30],'ID:')

        self.nameBox = self.create_textBox([300,ld[0]],[300,40],'box_ss')
        self.attributesBox = self.create_comboBox([300,ld[1]],[300,40],'attributesBox',attributes,icons=icons_attributes)
        self.racesBox = self.create_comboBox([300,ld[2]],[300,40],'box_ss',races,readOnly=False)
        self.ratingsBox = self.create_comboBox([300,ld[3]],[300,40],'box_ss',ratings)
        self.ranksBox = self.create_comboBox([300,ld[4]],[100,40],'box_ss',ranks)
        self.uploadBox = self.create_button([300,ld[5]],[160,40],buttons,' Upload',icon='icons//upload.png',fileOpen=True)
        self.backgroundsBox = self.create_comboBox([300,ld[6]],[300,40],'box_ss',backgrounds)
        self.mpBox = self.create_comboBox([300,ld[7]],[100,40],'box_ss',mp)
        self.cardPointsBox = self.create_comboBox([300,ld[8]],[100,40],'box_ss',card_points)
        self.idBox = self.create_textBox([300,ld[9]],[100,40],'box_ss')
        self.effectBox = self.create_comboBox([705,630],[200,30],'effect_box',['Effect:','Pack:','Description:'],alignCenter=False)
        self.effectBox1 = self.create_textBox([710,675],[350,40],'effect_box',alignCenter=False)
        self.effectBox2 = self.create_textBox([710,740],[350,40],'effect_box',alignCenter=False)

        self.create_button([795,45],[180,40],buttons,'Show card')
        self.effectBox1.setTextMargins(10,0,0,0)
        self.effectBox2.setTextMargins(10,0,0,0)
        self.box_list.extend((self.nameBox,self.attributesBox,self.racesBox,self.ratingsBox,self.ranksBox,self.uploadBox,
                        self.backgroundsBox,self.mpBox,self.cardPointsBox,self.idBox,self.effectBox,self.effectBox1,self.effectBox2))
        self.setStyleSheet(stylesheet)
        self.loadPreset(self.box_list)
        self.load_menu()
        self.load_window()
        
    def load_window(self):

        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon('icons//freyalogo.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.show()

    def create_label(self,pos:list,ss:str,dim:list,text:str):

        label = QLabel(self)
        if text is not None:
            label.setText(text)
        label.move(pos[0],pos[1])
        if ss is not None:
            label.setObjectName(ss)
        label.resize(dim[0],dim[1])

    def create_textBox(self,pos:list,dim:list,ss:str,alignCenter=True):

        textBox = QLineEdit(self)
        if ss is not None:
            textBox.setObjectName(ss)
        textBox.move(pos[0],pos[1])
        textBox.resize(dim[0],dim[1])
        if alignCenter:
            textBox.setAlignment(QtCore.Qt.AlignCenter)
        return textBox
    
    def create_comboBox(self,pos:list,dim:list,ss:str,items:list,readOnly=True,icons=None,alignCenter=True):

        comboBox = QComboBox(self)
        comboBox.setEditable(True)
        comboBox.setStyleSheet(down_arrow)
        if ss is not None:
            comboBox.setObjectName(ss)
        if icons is not None:
            if len(items) == 0:
                for icon in icons:
                    comboBox.addItem(QtGui.QIcon(icon), None)
            else:
                index = 0
                for icon in icons:
                    comboBox.addItem(QtGui.QIcon(icon),items[index])
                    index+=1
        else:
            comboBox.addItems(items)
        comboBox.move(pos[0],pos[1])
        comboBox.resize(dim[0],dim[1])
        if alignCenter:
            comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        comboBox.lineEdit().setReadOnly(readOnly)
        comboBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        return comboBox

    def create_button(self,pos:list,dim:list,ss:str,text:str,icon=None,fileOpen=False):

        self.button = QPushButton(text.strip(),self)
        self.button.setStyleSheet(ss)
        self.button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button.move(pos[0],pos[1])
        self.button.resize(dim[0],dim[1])
        self.button.setText(text)
        if icon is not None:
            self.button.setIcon(QtGui.QIcon(icon))
        if fileOpen:
            self.button.clicked.connect(self.loadImage)
        self.button.clicked.connect(self.clickButton)
        return self.button

    def load_menu(self):
    
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        configMenu = menubar.addMenu('&Config')

        loadAction = QtWidgets.QAction(QtGui.QIcon('icons//load.png'),'&Load', self)
        saveAction = QtWidgets.QAction(QtGui.QIcon('icons//save.png'),'&Save', self)
        generateAction = QtWidgets.QAction('&Generate card', self)
        helpAction = QtWidgets.QAction('&Help', self)
        self.fileFromPC = QtWidgets.QAction(QtGui.QIcon('icons//check.png'),'&Upload image from PC', self)
        self.fileFromWeb = QtWidgets.QAction('&Upload image from Web', self)

        loadAction.setShortcut('Ctrl+L')
        saveAction.setShortcut('Ctrl+S')
        generateAction.setShortcut('Ctrl+G')
        helpAction.setShortcut('Ctrl+H')
        self.fileFromPC.setShortcut('Ctrl+P')
        self.fileFromWeb.setShortcut('Ctrl+W')

        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        menubar.addAction(generateAction)
        menubar.addAction(helpAction)
        configMenu.addAction(self.fileFromPC)
        configMenu.addAction(self.fileFromWeb)

        loadAction.triggered.connect(self.loadFile)
        saveAction.triggered.connect(self.saveFile)
        generateAction.triggered.connect(self.saveImage)
        self.fileFromWeb.triggered.connect(self.changeModeWeb)
        self.fileFromPC.triggered.connect(self.changeModePc)

        self.styleSheet = Qmenu
        menubar.setStyleSheet(self.styleSheet)

    def loadFile(self):

        if len(self.dirJson["dir_load_file"]) == 0:
            dir = f'{QtCore.QDir.currentPath()}'
        else:
            dir = self.dirJson["dir_load_file"]
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Load file',
            directory=dir,
            filter='Data file (*.json)')
        if response[0]:
            self.dirJson["dir_load_file"] = response[0]
            jmanager.updateJson('data//data.json', data=self.dirJson)
            self.lastEditionJson = jmanager.readJson(response[0])
            self.loadPreset(self.box_list)

    def saveFile(self):
        
        if len(self.dirJson["dir_save_file"]) == 0:
            dir = f'{QtCore.QDir.currentPath()}'
        else:
            dir = self.dirJson["dir_save_file"]
        newDir = f'{dir.replace(basename(dir),"")}{self.idBox.text()} - {self.nameBox.text()}.json'
        response = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory=newDir,
            filter='Data file (*.json)')
        if response[0]:
            self.dirJson["dir_save_file"] = response[0]
            self.savePreset(self.box_list)
            jmanager.createJson(response[0], self.lastEditionJson)
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def loadImage(self):

        if len(self.dirJson["dir_upload_image"]) == 0:
            dir = f'{QtCore.QDir.currentPath()}'
        else:
            dir = self.dirJson["dir_upload_image"]
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Load file',
            directory=dir,
            filter='Images (*.png;*.jpg;*.gif)')
        if response[0]:
            self.dirJson["dir_upload_image"] = response[0]
            self.imageDir = response[0]
        self.savePreset(self.box_list)
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def saveImage(self):

        if len(self.dirJson["dir_save_image"]) == 0:
            dir = f'{QtCore.QDir.currentPath()}'
        else:
            dir = self.dirJson["dir_save_image"]
        imgFormat = '.png'
        for imgForm in self.imageFormats:
            if imgForm in self.imgPreset:
                imgFormat = imgForm
        newDir = f'{dir.replace(basename(dir),"")}{self.idBox.text()} - {self.nameBox.text()}{imgFormat}'
        response = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory=newDir,
            filter='Images (*.png;*.jpg;*.gif)')
        if response[0]:
            self.dirJson["dir_save_image"] = response[0]
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def clickButton(self):

        self.savePreset(self.box_list)

    def loadPreset(self, boxes:list):

        keys = list(self.lastEditionJson.keys())
        i = 0
        for box in boxes:
            if isinstance(box, QComboBox):
                if box.objectName() == 'attributesBox':
                    index = 0
                    for att in attributes:
                        if att == self.lastEditionJson[keys[i]]:
                            box.setCurrentIndex(index)
                        index+=1
                else:
                    box.setCurrentText(self.lastEditionJson[keys[i]])
            elif isinstance(box, QLineEdit):
                box.setText(self.lastEditionJson[keys[i]])
            else:
                self.imageDir = self.lastEditionJson[keys[i]]
            i+=1
    
    def savePreset(self, boxes:list):

        i = 0
        for key in self.lastEditionJson:
            if isinstance(boxes[i], QComboBox):
                self.lastEditionJson[key] = boxes[i].currentText()
            else:
                self.lastEditionJson[key] = boxes[i].text()
            i+=1
        self.lastEditionJson['Image'] = self.imageDir
        jmanager.updateJson('presets//last_edition.json', self.lastEditionJson)

    def changeModePc(self):

        icon = QtGui.QIcon('icons//check.png')
        noneIcon = QtGui.QIcon('')
        self.fileFromPC.setIcon(icon)
        self.fileFromWeb.setIcon(noneIcon)
        self.dialogUploadIsFromWeb = False

    def changeModeWeb(self):

        noneIcon = QtGui.QIcon('')
        icon = QtGui.QIcon('icons//check.png')
        self.fileFromWeb.setIcon(icon)
        self.fileFromPC.setIcon(noneIcon)
        self.dialogUploadIsFromWeb = True

def runApp():

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
    

runApp()