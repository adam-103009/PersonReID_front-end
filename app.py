from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog , QTextEdit
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
from UI import UI_MainWindow
import json_preprocess
import cv2
import numpy as np
import pathlib
import os 

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.dic1_personID_Frame={}
        self.dic2_personID_Frame={}
        self.filename1 = ""     # extract same person's images
        self.filename2 = ""     # extract same person's images
        self.getrecord1 = False
        self.getrecord2 = False
        self.list1_personID_Valid_Frame = []
        self.list2_personID_Valid_Frame = []
        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        #p =self.palette()
        #p.setColor(QPalette.Window, Qt.black)
        #self.setPalette(p)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.perosonID_TxitEdit=""
        self.ui = UI_MainWindow()
        self.ui.setUI(self)

        #signal handle
        self.ui.openBtn_1.clicked.connect(partial(self.open_file,1))
        self.ui.openBtn_2.clicked.connect(partial(self.open_file,2))
        self.ui.timeBtn.clicked.connect(self.input_time)
        self.ui.playBtn_1.clicked.connect(partial(self.play_video,1))
        self.ui.playBtn_2.clicked.connect(partial(self.play_video,2))
        self.ui.slider_1.sliderMoved.connect(self.set_position_1)
        self.ui.slider_2.sliderMoved.connect(self.set_position_2)
        self.ui.mediaPlayer_1.stateChanged.connect(partial(self.mediastate_changed,1))
        self.ui.mediaPlayer_1.positionChanged.connect(self.position_changed_1)
        self.ui.mediaPlayer_1.durationChanged.connect(self.duration_changed_1)
        self.ui.mediaPlayer_2.stateChanged.connect(partial(self.mediastate_changed,2))
        self.ui.mediaPlayer_2.positionChanged.connect(self.position_changed_2)
        self.ui.mediaPlayer_2.durationChanged.connect(self.duration_changed_2)

        self.ui.playBtn_1.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.playBtn_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.get_frameBtn.clicked.connect(self.get_frame)
        self.ui.get_frameBtn.clicked.connect(self.extract_pimage)

        self.setLayout(self.ui.hboxLayout_all)
    def get_frame(self):
        t=self.ui.personID_TextEdit.toPlainText()
        if(t in self.dic1_personID_Frame):
            output="Video 1 :\nTime             Frame\n"+self.dic1_personID_Frame[t]
            self.ui.showFrame_label.setText(output)
        if(t in self.dic2_personID_Frame):
            print("self.dic2_personID_Frame : ", self.dic2_personID_Frame)
            output="Video 2 :\nTime             Frame\n"+self.dic2_personID_Frame[t]
            self.ui.showFrame2_label.setText(output)
        return
    def open_file(self,n):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            if n==1:
                #get the video fps
                self.getrecord1 = True
                self.filename1 = filename
                cap=cv2.VideoCapture(filename)
                self.video1_fps=cap.get(cv2.CAP_PROP_FPS)
                get_personID=json_preprocess.show_personID(1)
                self.list1_personID_Valid_Frame =get_personID
                c=0 #每5個id一行
                for i in range(len(get_personID)):
                    frame=json_preprocess.get_personExitFrame(1,get_personID[i],self.video1_fps)
                    self.dic1_personID_Frame.update({get_personID[i]:frame})
                    if(i==0):
                        self.perosonID_TxitEdit=self.perosonID_TxitEdit+get_personID[i]+" : \n"
                    else:
                        self.perosonID_TxitEdit=self.perosonID_TxitEdit+get_personID[i]+"    "
                    if(c==5):
                        c=0
                        self.perosonID_TxitEdit=self.perosonID_TxitEdit+"\n"
                    c=c+1
                self.ui.mediaPlayer_1.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.ui.playBtn_1.setEnabled(True)
                self.ui.window1_personID.setText(self.perosonID_TxitEdit)
                self.perosonID_TxitEdit=self.perosonID_TxitEdit+"\n"
            elif n==2:
                #get the video fps
                self.getrecord2 = True
                self.filename2 = filename
                cap=cv2.VideoCapture(filename)
                self.video2_fps=cap.get(cv2.CAP_PROP_FPS)
                self.perosonID_TxitEdit=""
                get_personID=json_preprocess.show_personID(2)
                self.list2_personID_Valid_Frame =get_personID
                c=0 #每5個id一行
                for i in range(len(get_personID)):
                    frame=json_preprocess.get_personExitFrame(2,get_personID[i],self.video2_fps)
                    self.dic2_personID_Frame.update({get_personID[i]:frame})
                    if(i==0):
                        self.perosonID_TxitEdit=self.perosonID_TxitEdit+get_personID[i]+" : \n"
                    else:
                        self.perosonID_TxitEdit=self.perosonID_TxitEdit+get_personID[i]+"    "
                    if(c==5):
                        c=0
                        self.perosonID_TxitEdit=self.perosonID_TxitEdit+"\n"
                    c=c+1
                self.ui.mediaPlayer_2.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.ui.playBtn_2.setEnabled(True)
                self.ui.window2_personID.setText(self.perosonID_TxitEdit)
    def input_time(self):
        t=self.ui.text_box.toPlainText()
        if(t!=""):
            t=int(t)/self.video1_fps*501
            self.ui.mediaPlayer_1.setPosition(int(t))

        t2=self.ui.window2_timeInput.toPlainText()
        if(t2!=""):
            t2=int(t2)/self.video2_fps*501
            self.ui.mediaPlayer_2.setPosition(int(t2))
    def play_video(self,window_num):
        if window_num==1:
            if self.ui.mediaPlayer_1.state() == QMediaPlayer.PlayingState:
                self.ui.mediaPlayer_1.pause()

            else:
                self.ui.mediaPlayer_1.play()
        elif window_num==2:
            if self.ui.mediaPlayer_2.state() == QMediaPlayer.PlayingState:
                self.ui.mediaPlayer_2.pause()
            else:
                self.ui.mediaPlayer_2.play()
    def mediastate_changed(self, window_num):
        if window_num==1:
            if self.ui.mediaPlayer_1.state() == QMediaPlayer.PlayingState:
                self.ui.playBtn_1.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause)

                )

            else:
                self.ui.playBtn_1.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay)
                )
        elif window_num==2:
            if self.ui.mediaPlayer_2.state() == QMediaPlayer.PlayingState:
                self.ui.playBtn_2.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause)

                )

            else:
                self.ui.playBtn_2.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay)

                )
    def position_changed_1(self, position):
        self.ui.slider_1.setValue(position)
        #將position數值轉換成時間，1秒為1002
        value_s=int(position/1002)
        if(value_s%60>=10):
            s=str(int(value_s%60))
        else:
            s="0"+str(int(value_s%60))
        m=str(int(value_s/60))
        self.ui.window1_durationTime.setText(m+":"+s)
    def position_changed_2(self, position):
        self.ui.slider_2.setValue(position)
        #將position數值轉換成時間，1秒為1002
        value_s=int(position/1002)
        if(value_s%60>10):
            s=str(int(value_s%60))
        else:
            s="0"+str(int(value_s%60))
        m=str(int(value_s/60))
        self.ui.window2_durationTime.setText(m+":"+s)
    def duration_changed_1(self, duration):
        self.ui.slider_1.setRange(0, duration)
        #return
    def duration_changed_2(self, duration):
        self.ui.slider_2.setRange(0, duration)
        #return
    def set_position_1(self, position):
        print(position)
        self.ui.mediaPlayer_1.setPosition(position)
    def set_position_2(self, position):
        self.ui.mediaPlayer_2.setPosition(position)

    def extract_pimage(self):
        # get current working dir path
        cpath = pathlib.Path(__file__).parent.resolve()
        # build new dir (store images query)
        # video 1
        if self.getrecord1 == True:
            newpath = str(cpath) + "\images1"
            frame_count = 0
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            cap = cv2.VideoCapture(self.filename1)
            valid_pbbox = json_preprocess.get_bbox(self.list1_personID_Valid_Frame)
            query_pid=self.ui.personID_TextEdit.toPlainText()
            for pid_detail in valid_pbbox:
                if pid_detail[0] == query_pid:
                    # just read the first frame of each person  
                    # init var 
                    count_len = 0
                    img_name = 0
                    while(cap.isOpened()):
                        frame_count += 2
                        ret, frame = cap.read()
                        # extract the img of target person
                        if count_len < len(pid_detail[1]):
                            if frame_count == pid_detail[1][count_len][0]:
                                x, y, w, h = pid_detail[1][count_len][1][0], pid_detail[1][count_len][1][1], pid_detail[1][count_len][1][2], pid_detail[1][count_len][1][3]
                                x1, x2, y1, y2 = x, (x+w), y, (y+h) 
                                ext_bbox = frame[y1:y2, x1:x2]
                                # magnify the person extracted !
                                scale_percent = 500
                                width = int(ext_bbox.shape[1] * scale_percent / 100)
                                height = int(ext_bbox.shape[0] * scale_percent / 100)
                                dim = (width, height)
                                ext_bbox = cv2.resize(ext_bbox, dim, interpolation = cv2.INTER_AREA)
                                cv2.imwrite(f'{cpath}\images1\image_{img_name}.png',ext_bbox)
                                img_name += 1
                                count_len += 1
                        else : 
                            break
                else:
                    continue
        

        # build new dir (store images query)
        # video 2
        if self.getrecord2 == True:
            newpath = str(cpath) + "\images2" 
            frame_count = 0
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            cap = cv2.VideoCapture(self.filename2)
            valid_pbbox = json_preprocess.get_bbox(self.list2_personID_Valid_Frame)
            query_pid=self.ui.personID_TextEdit.toPlainText()
            for pid_detail in valid_pbbox:
                if pid_detail[0] == query_pid:
                    # just read the first frame of each person  
                    # init var 
                    count_len = 0
                    img_name = 0
                    while(cap.isOpened()):
                        frame_count += 2
                        ret, frame = cap.read()
                        # extract the img of target person
                        if count_len < len(pid_detail[1]):
                            if frame_count == pid_detail[1][count_len][0]:
                                x, y, w, h = pid_detail[1][count_len][1][0], pid_detail[1][count_len][1][1], pid_detail[1][count_len][1][2], pid_detail[1][count_len][1][3]
                                x1, x2, y1, y2 = x, (x+w), y, (y+h) 
                                ext_bbox = frame[y1:y2, x1:x2]
                                # magnify the person extracted !
                                scale_percent = 500
                                width = int(ext_bbox.shape[1] * scale_percent / 100)
                                height = int(ext_bbox.shape[0] * scale_percent / 100)
                                dim = (width, height)
                                ext_bbox = cv2.resize(ext_bbox, dim, interpolation = cv2.INTER_AREA)
                                cv2.imwrite(f'{cpath}\images2\image_{img_name}.png',ext_bbox)
                                img_name += 1
                                count_len += 1
                        else : 
                            break
                else:
                    continue


        
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())