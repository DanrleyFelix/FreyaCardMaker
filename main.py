import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,QMessageBox,
QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QScrollArea, QComboBox)
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QRect,Qt
from utils import *
from style import *
from json_manager import JsonManager
from os.path import basename,realpath
from images import Card
from webbrowser import open as opw


jmanager = JsonManager()
app = QApplication(sys.argv)


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.top = 0
        self.left = 0
        self.width = 1080
        self.height = 833
        self.setMaximumWidth(1080)
        self.setMinimumWidth(833)
        self.setMaximumHeight(833)
        self.setMinimumHeight(600)
        self.title = "Freya Card Maker"
        stylesheet = ""
        self.checkIcon = QtGui.QIcon('icons//check.png')
        self.noneIcon = QtGui.QIcon('')
        self.lastEditionJson = jmanager.readJson('presets//last_edition.json')
        self.dirJson = jmanager.readJson('data//data.json')
        self.dialogUploadIsFromWeb = bool(int(self.dirJson['upload_web']))
        self.previewImageQualityIsHigh = bool(int(self.dirJson['high_quality_preview']))
        self.imageDir = ''
        self.imageFormats = ['.png','.gif']
        self.box_list = []
        self.label_list = []
        self.imgPreset = f"interface//{self.dirJson['last_show_image']}"
        with open("design.qss", "r") as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)
        self.loadScrollArea()
        self.loadPreset(self.box_list)
        self.loadMenu()
        self.load_window()
        
    def load_window(self):

        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon('icons//freyalogo.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

    def loadScrollArea(self):
        
        layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(False)
        self.widget = QWidget(self.scrollArea)
        self.widget.setGeometry(QRect(0,0,1080,800))
        self.loadInterface(self.widget)
        self.scrollArea.setWidget(self.widget)
        layout.addWidget(self.widget)
        self.scrollLayout = QVBoxLayout(self.widget)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(layout)

    def loadInterface(self,widget):

        self.interface = QLabel(widget)
        interface_backgropund = QtGui.QPixmap('interface//background.png')
        self.interface.setPixmap(interface_backgropund)
        self.labelCardImg = QLabel(self.widget)
        self.interface.resize(1080,800)
        self.labelCardImg.move(675,70)
        self.labelCardImg.resize(370,520)
        self.loadCardLabel()
        # Labels
        ld = label_distance(70,800,70)
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
        x_distance = 285
        self.nameBox = self.create_textBox([x_distance,ld[0]],[300,40],'box_ss')
        self.attributesBox = self.create_comboBox([x_distance,ld[1]],[300,40],'attributesBox',attributes,icons=icons_attributes)
        self.racesBox = self.create_comboBox([x_distance,ld[2]],[300,40],'box_ss',races,readOnly=False)
        self.ratingsBox = self.create_comboBox([x_distance,ld[3]],[300,40],'box_ss',ratings)
        self.ranksBox = self.create_comboBox([x_distance,ld[4]],[100,40],'box_ss',ranks)
        self.uploadBox = self.create_button([x_distance,ld[5]],[160,40],buttons,' Upload',icon='icons//upload.png',fileOpen=True)
        self.backgroundsBox = self.create_comboBox([x_distance,ld[6]],[300,40],'box_ss',backgrounds)
        self.mpBox = self.create_comboBox([x_distance,ld[7]],[100,40],'box_ss',mp)
        self.cardPointsBox = self.create_comboBox([x_distance,ld[8]],[100,40],'box_ss',card_points)
        self.idBox = self.create_textBox([x_distance,ld[9]],[100,40],'box_ss')
        self.effectBox = self.create_comboBox([680,600],[145,35],'effect_box2',['Effect: ','Pack: ','Description: '],alignCenter=False)
        self.effectBox1 = self.create_textBox([685,645],[350,40],'effect_box',alignCenter=False)
        self.effectBox2 = self.create_textBox([685,710],[350,40],'effect_box',alignCenter=False)

        self.create_button([775,15],[180,40],buttons,'Show card')
        self.effectBox1.setTextMargins(10,0,0,0)
        self.effectBox2.setTextMargins(10,0,0,0)

    def create_label(self,pos:list,ss:str,dim:list,text:str):

        label = QLabel(self.widget)
        if text is not None:
            label.setText(text)
        label.move(pos[0],pos[1])
        if ss is not None:
            label.setObjectName(ss)
        label.resize(dim[0],dim[1])
        self.label_list.append(label)

    def create_textBox(self,pos:list,dim:list,ss:str,alignCenter=True):

        textBox = QLineEdit(self.widget)
        if ss is not None:
            textBox.setObjectName(ss)
        textBox.move(pos[0],pos[1])
        textBox.resize(dim[0],dim[1])
        if alignCenter:
            textBox.setAlignment(QtCore.Qt.AlignCenter)
        self.box_list.append(textBox)
        return textBox
    
    def create_comboBox(self,pos:list,dim:list,ss:str,items:list,readOnly=True,icons=None,alignCenter=True):

        comboBox = QComboBox(self.widget)
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
        self.box_list.append(comboBox)
        return comboBox

    def create_button(self,pos:list,dim:list,ss:str,text:str,icon=None,fileOpen=False):

        self.button = QPushButton(text.strip(),self.widget)
        self.button.setStyleSheet(ss)
        self.button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button.move(pos[0],pos[1])
        self.button.resize(dim[0],dim[1])
        self.button.setText(text)
        if icon is not None:
            self.button.setIcon(QtGui.QIcon(icon))
        if fileOpen:
            self.button.clicked.connect(self.loadImage)
        else:
            self.button.clicked.connect(self.clickButton)
        if 'upload' in text.lower():
            self.box_list.append(self.button)
        return self.button

    def loadMenu(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        configMenu = menubar.addMenu('&Config')
        helpMenuBar = menubar.addMenu('Help')

        loadAction = QtWidgets.QAction(QtGui.QIcon('icons//load.png'),'&Load', self)
        saveAction = QtWidgets.QAction(QtGui.QIcon('icons//save.png'),'&Save', self)
        generateAction = QtWidgets.QAction('&Generate card', self)
        helpActionUS = QtWidgets.QAction(QtGui.QIcon('icons//us.png'),'&EN-US', self)
        helpActionBR = QtWidgets.QAction(QtGui.QIcon('icons//brazil.png'),'&PT-BR', self)
        self.fileFromPC = QtWidgets.QAction('&Upload image from PC', self)
        self.fileFromWeb = QtWidgets.QAction('&Upload image from Web', self)
        self.showImageLow = QtWidgets.QAction('&Low quality gif', self)
        self.showImageHigh = QtWidgets.QAction('&High quality gif', self)
        self.onlySpace = QtWidgets.QAction('--------------------------', self)
        if self.dialogUploadIsFromWeb:
            self.fileFromWeb.setIcon(self.checkIcon)
        else:
            self.fileFromPC.setIcon(self.checkIcon)
        if self.previewImageQualityIsHigh:
            self.showImageHigh.setIcon(self.checkIcon)
        else:
            self.showImageLow.setIcon(self.checkIcon)
        loadAction.setShortcut('Ctrl+O')
        saveAction.setShortcut('Ctrl+S')
        generateAction.setShortcut('Ctrl+G')
        self.fileFromPC.setShortcut('Ctrl+P')
        self.fileFromWeb.setShortcut('Ctrl+W')
        self.showImageLow.setShortcut('Ctrl+L')
        self.showImageHigh.setShortcut('Ctrl+K')

        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        menubar.addAction(generateAction)
        helpMenuBar.addAction(helpActionBR)
        helpMenuBar.addAction(helpActionUS)
        configMenu.addAction(self.fileFromPC)
        configMenu.addAction(self.fileFromWeb)
        configMenu.addAction(self.onlySpace)
        configMenu.addAction(self.showImageHigh)
        configMenu.addAction(self.showImageLow)

        loadAction.triggered.connect(self.loadFile)
        saveAction.triggered.connect(self.saveFile)
        generateAction.triggered.connect(self.saveImage)
        helpActionUS.triggered.connect(self.openHelpDialogUS)
        helpActionBR.triggered.connect(self.openHelpDialogBR)
        self.fileFromWeb.triggered.connect(self.changeModeWeb)
        self.fileFromPC.triggered.connect(self.changeModePc)
        self.showImageLow.triggered.connect(self.changeModeLow)
        self.showImageHigh.triggered.connect(self.changeModeHigh)

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

    def loadCardLabel(self):
        
        self.dirJson = jmanager.readJson('data//data.json')
        self.imgPreset = f"interface//{self.dirJson['last_show_image']}"
        if 'gif' in self.imgPreset:
            self.movie = QtGui.QMovie(self.imgPreset)
            self.labelCardImg.setMovie(self.movie)
            self.movie.start()
        else:
            pngImage = QtGui.QPixmap(self.imgPreset)
            self.labelCardImg.setPixmap(pngImage)

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
            self.savePreset(self.box_list,onlyFile=True)
            jmanager.createJson(response[0], self.lastEditionJson)
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def loadImage(self):

        card = Card()
        if card.totalFrames > 1:
            self.dirJson["last_show_image"] = 'temp.gif'
        elif card.totalFrames == 1:
            self.dirJson["last_show_image"] = 'temp.png'
        if self.dialogUploadIsFromWeb:
            self.showDialogWebMode()
        else:
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
        self.savePreset(self.box_list, onlyFile=True)
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
            caption='Save Image',
            directory=newDir,
            filter='Images (*.png;*.gif)')
        app.setOverrideCursor(Qt.WaitCursor)
        if response[0]:
            self.dirJson["dir_save_image"] = response[0]
            card = Card()
            uploadState = card.uploadImages()
            if uploadState == False:
                app.restoreOverrideCursor()
                return self.show_critical_messagebox()
            card.saveImage(response[0])
        app.restoreOverrideCursor()
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def show_critical_messagebox(self,msg='Upload another Image!'):

        messageBox = QMessageBox()
        messageBox.critical(self,'Critical Error',msg,QMessageBox.Ok) 
    
    def show_info_messagebox(self):

        msg = QMessageBox()
        msg.information(self,'Information','The gif will take a long time to load the preview. Colors may be grayer.',QMessageBox.Ok) 

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
    
    def savePreset(self, boxes:list, onlyFile=False):

        i = 0
        for key in self.lastEditionJson:
            if isinstance(boxes[i], QComboBox):
                self.lastEditionJson[key] = boxes[i].currentText()
            else:
                self.lastEditionJson[key] = boxes[i].text()
            i+=1
        self.lastEditionJson['Image'] = self.imageDir
        jmanager.updateJson('presets//last_edition.json', self.lastEditionJson)
        app.setOverrideCursor(Qt.WaitCursor)
        if not onlyFile:
            card = Card()
            try:
                card.uploadImages()
                card.saveImageTemp()
                self.loadCardLabel()
            except Exception as e:
                msg = str(e)
                app.restoreOverrideCursor()
                self.show_critical_messagebox(msg=msg)
        app.restoreOverrideCursor()

    def changeModePc(self):


        self.fileFromPC.setIcon(self.checkIcon)
        self.fileFromWeb.setIcon(self.noneIcon)
        self.dialogUploadIsFromWeb = False
        self.dirJson['upload_web'] = "0"
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def changeModeWeb(self):

        self.fileFromWeb.setIcon(self.checkIcon)
        self.fileFromPC.setIcon(self.noneIcon)
        self.dialogUploadIsFromWeb = True
        self.dirJson['upload_web'] = "1"
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def changeModeLow(self):

        self.showImageLow.setIcon(self.checkIcon)
        self.showImageHigh.setIcon(self.noneIcon)
        self.previewImageQualityIsHigh = False
        self.dirJson['high_quality_preview'] = "0"
        jmanager.updateJson('data//data.json', data=self.dirJson)

    def changeModeHigh(self):

        self.showImageHigh.setIcon(self.checkIcon)
        self.showImageLow.setIcon(self.noneIcon)
        self.previewImageQualityIsHigh = True
        self.dirJson['high_quality_preview'] = "1"
        jmanager.updateJson('data//data.json', data=self.dirJson)
        self.show_info_messagebox()

    def showDialogWebMode(self):
        text,check = QtWidgets.QInputDialog.getText(self, 'Upload','Image URL:',flags=QtCore.Qt.WindowCloseButtonHint)

        if check:
            self.imageDir = text
            self.lastEditionJson['Image'] = self.imageDir
            jmanager.updateJson('presets//last_edition.json', self.lastEditionJson)

    def openHelpDialogBR(self):
        
        try:
            opw('file://' + realpath('index/index.html'))
        except Exception as e:
            msg = str(e)
            self.show_critical_messagebox(msg=msg)

    def openHelpDialogUS(self):
        
        try:
            opw('file://' + realpath('index/index_us.html'))
        except Exception as e:
            msg = str(e)
            self.show_critical_messagebox(msg=msg)

        
def runApp():

    window = Window()
    window.show()
    sys.exit(app.exec())
    

runApp()