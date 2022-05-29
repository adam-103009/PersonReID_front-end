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

        #create label to show all person ID who exit more than 20 frame
        self.window1_personID=QLabel()
        self.window2_personID=QLabel()
        self.window1_personID.setAlignment(Qt.AlignTop)
        self.window2_personID.setAlignment(Qt.AlignTop)
        self.showFrame_label = QLabel()
        self.showFrame2_label = QLabel()
        self.showFrame_label.setAlignment(Qt.AlignTop)
        self.showFrame2_label.setAlignment(Qt.AlignTop)
        self.note_output_ID_label=QLabel("All person's ID in left two video")
        self.note_input_ID_label=QLabel("Please input person's ID whom you want to find")
        self.note_output_Frame_label=QLabel("The time that this person appear in")
        self.note_input_Frame_label=QLabel("Please input the time which you want to watch")
        self.window1_durationTime=QLabel()
        self.window2_durationTime=QLabel()
        #self.window1_personID.setText("test")
        #create open button
        self.openBtn_1 = QPushButton('Open Video')

        self.openBtn_2 = QPushButton('Open Video 2')

        #time input button
        self.timeBtn = QPushButton("time input")
        #get frame button
        self.get_frameBtn = QPushButton("Get frame")

        #show frame button
        self.video1_showframeBtn=[]
        self.video2_showframeBtn=[]
        for i in range(15):
            self.video1_showframeBtn.append(QPushButton(""))
            self.video2_showframeBtn.append(QPushButton(""))
        #input text
        self.text_box = QTextEdit()
        self.window2_timeInput = QTextEdit()
        self.personID_TextEdit = QTextEdit()
        #create button for playing
        self.playBtn_1 = QPushButton()
        self.playBtn_1.setEnabled(False)
    
    

        self.playBtn_2 = QPushButton()
        self.playBtn_2.setEnabled(False)
        




        #create slider
        self.slider_1 = QSlider(Qt.Horizontal)
        #self.slider_1.setRange(0,126369)
        self.slider_1.setRange(0,0)
        self.slider_2 = QSlider(Qt.Horizontal)
        #self.slider_2.setRange(0,191520)
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
        hboxLayout_1.addWidget(self.window1_durationTime)

        hboxLayout_2.addWidget(self.openBtn_2)
        hboxLayout_2.addWidget(self.playBtn_2)
        hboxLayout_2.addWidget(self.slider_2)
        hboxLayout_2.addWidget(self.window2_durationTime)

        #showing person ID layout
        showPersonID = QHBoxLayout()
        showPersonID.setContentsMargins(0,0,0,0)
        showPersonID.addWidget(self.window1_personID)
        showPersonID.addWidget(self.window2_personID)

        showExitTime = QHBoxLayout()
        showExitTime.setContentsMargins(0,0,0,0)
        showExitTime.addWidget(self.personID_TextEdit)
        showExitTime.addWidget(self.get_frameBtn)

        inputTime = QHBoxLayout()
        inputTime.setContentsMargins(0,0,0,0)
        inputTime.addWidget(self.text_box)
        inputTime.addWidget(self.window2_timeInput)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.videowidget_1)
        vboxLayout.addLayout(hboxLayout_1)
        vboxLayout.addWidget(self.videowidget_2)
        vboxLayout.addLayout(hboxLayout_2)
        vboxLayout.setStretch(0,7)
        vboxLayout.setStretch(1,1)
        vboxLayout.setStretch(2,7)
        vboxLayout.setStretch(3,1)

        video1_showFrameBtn = QVBoxLayout()
        video1_showFrameBtn.setContentsMargins(0,0,0,0)
        for i in range(15):
            video1_showFrameBtn.addWidget(self.video1_showframeBtn[i])

        video2_showFrameBtn = QVBoxLayout()
        video2_showFrameBtn.setContentsMargins(0,0,0,0)
        for i in range(15):
            video2_showFrameBtn.addWidget(self.video2_showframeBtn[i])

        showFrame = QHBoxLayout()
        showFrame.setContentsMargins(0,0,0,0)
        showFrame.addWidget(self.showFrame_label)
        showFrame.addLayout(video1_showFrameBtn)
        showFrame.addWidget(self.showFrame2_label)
        showFrame.addLayout(video2_showFrameBtn)

        vboxLayout_3 = QVBoxLayout()
        vboxLayout_3.addWidget(self.note_output_ID_label)
        vboxLayout_3.addLayout(showPersonID)
        vboxLayout_3.addWidget(self.note_input_ID_label)
        vboxLayout_3.addLayout(showExitTime)
        vboxLayout_3.addWidget(self.note_output_Frame_label)
        vboxLayout_3.addLayout(showFrame)
        vboxLayout_3.addWidget(self.note_input_Frame_label)
        vboxLayout_3.addLayout(inputTime)
        vboxLayout_3.addWidget(self.timeBtn)
        vboxLayout_3.setStretch(0,1)
        vboxLayout_3.setStretch(1,1)
        vboxLayout_3.setStretch(2,1)
        vboxLayout_3.setStretch(3,1)
        vboxLayout_3.setStretch(4,1)
        vboxLayout_3.setStretch(5,4)
        vboxLayout_3.setStretch(6,1)
        vboxLayout_3.setStretch(7,1)
        vboxLayout_3.setStretch(8,1)

        self.hboxLayout_all = QHBoxLayout()
        self.hboxLayout_all.setContentsMargins(0,0,0,0)
        self.hboxLayout_all.addLayout(vboxLayout)
        self.hboxLayout_all.addLayout(vboxLayout_3)
        
        self.mediaPlayer_1.setVideoOutput(self.videowidget_1)
        self.mediaPlayer_2.setVideoOutput(self.videowidget_2)