from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog , QTextEdit
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
class UI_MainWindow(object):
    def setUI(self, MainWidow):
        #create media player object
        self.mediaPlayer_1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer_2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create videowidget object

        self.videowidget_1 = QVideoWidget()
        self.videowidget_2 = QVideoWidget()

        #create open button
        self.openBtn_1 = QPushButton('Open Video')

        self.openBtn_2 = QPushButton('Open Video 2')

        #time input button
        self.timeBtn = QPushButton("time input")

        #input text
        self.text_box = QTextEdit()

        #create button for playing
        self.playBtn_1 = QPushButton()
        self.playBtn_1.setEnabled(False)
    
    

        self.playBtn_2 = QPushButton()
        self.playBtn_2.setEnabled(False)
        




        #create slider
        self.slider_1 = QSlider(Qt.Horizontal)
        self.slider_1.setRange(0,0)

        self.slider_2 = QSlider(Qt.Horizontal)
        self.slider_2.setRange(0,0)


        #create hbox layout
        hboxLayout_1 = QHBoxLayout()
        hboxLayout_1.setContentsMargins(0,0,0,0)

        hboxLayout_2 = QHBoxLayout()
        hboxLayout_2.setContentsMargins(0,0,0,0)

        #UI 排版
        hboxLayout_1.addWidget(self.openBtn_1)
        hboxLayout_1.addWidget(self.playBtn_1)
        hboxLayout_1.addWidget(self.slider_1)

        hboxLayout_2.addWidget(self.openBtn_2)
        hboxLayout_2.addWidget(self.playBtn_2)
        hboxLayout_2.addWidget(self.slider_2)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.videowidget_1)
        vboxLayout.addLayout(hboxLayout_1)
        vboxLayout.addWidget(self.videowidget_2)
        vboxLayout.addLayout(hboxLayout_2)

        vboxLayout_3 = QVBoxLayout()
        vboxLayout_3.addWidget(self.text_box)
        vboxLayout_3.addWidget(self.timeBtn)

        self.hboxLayout_all = QHBoxLayout()
        self.hboxLayout_all.setContentsMargins(0,0,0,0)
        self.hboxLayout_all.addLayout(vboxLayout)
        self.hboxLayout_all.addLayout(vboxLayout_3)
        
        self.mediaPlayer_1.setVideoOutput(self.videowidget_1)
        self.mediaPlayer_2.setVideoOutput(self.videowidget_2)