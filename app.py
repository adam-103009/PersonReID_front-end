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
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.dic1_personID_Frame={}
        self.dic2_personID_Frame={}
        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        #p =self.palette()
        #p.setColor(QPalette.Window, Qt.black)
        #self.setPalette(p)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.perosonID_TxitEdict=""
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
        self.setLayout(self.ui.hboxLayout_all)
    def get_frame(self):
        t=self.ui.personID_TextEdict.toPlainText()
        output=""
        if(t in self.dic1_personID_Frame):
            output=output+"Video 1 :"+self.dic1_personID_Frame[t]+"\n"
        if(t in self.dic2_personID_Frame):
            output=output+"Video 2 :"+self.dic2_personID_Frame[t]
        self.ui.showFrame_label.setText(output)
        return
    def open_file(self,n):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            if n==1:
                get_personID=json_preprocess.show_personID(1)
                for i in range(len(get_personID)):
                    frame=json_preprocess.get_personExitFrame(1,get_personID[i])
                    self.dic1_personID_Frame.update({get_personID[i]:frame})
                    self.perosonID_TxitEdict=self.perosonID_TxitEdict+get_personID[i]+"\n"
                self.ui.mediaPlayer_1.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.ui.playBtn_1.setEnabled(True)
                self.ui.window1_personID.setText(self.perosonID_TxitEdict)
                self.perosonID_TxitEdict=self.perosonID_TxitEdict+"\n"
            elif n==2:
                self.perosonID_TxitEdict=""
                get_personID=json_preprocess.show_personID(2)
                for i in range(len(get_personID)):
                    frame=json_preprocess.get_personExitFrame(2,get_personID[i])
                    self.dic2_personID_Frame.update({get_personID[i]:frame})
                    self.perosonID_TxitEdict=self.perosonID_TxitEdict+get_personID[i]+"\n"
                self.ui.mediaPlayer_2.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.ui.playBtn_2.setEnabled(True)
                self.ui.window2_personID.setText(self.perosonID_TxitEdict)
    def input_time(self):
        t=self.ui.text_box.toPlainText()
        if(t!=""):
            t=int(t)/38*1002
            self.ui.mediaPlayer_1.setPosition(int(t))

        t2=self.ui.window2_timeInput.toPlainText()
        if(t2!=""):
            t2=int(t2)/50*1002
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
    def position_changed_2(self, position):
        self.ui.slider_2.setValue(position)

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





app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())