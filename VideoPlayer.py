from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog , QTextEdit
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl


#function 後面有加上1或2，分別代表上window和下window
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()


        self.show()


    def init_ui(self):

        #create media player object
        self.mediaPlayer_1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer_2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create videowidget object

        videowidget_1 = QVideoWidget()
        videowidget_2 = QVideoWidget()

        #create open button
        openBtn_1 = QPushButton('Open Video')
        openBtn_1.clicked.connect(self.open_file_1)

        openBtn_2 = QPushButton('Open Video 2')
        openBtn_2.clicked.connect(self.open_file_2)

        #time input button
        timeBtn = QPushButton("time input")
        timeBtn.clicked.connect(self.input_time)

        #input text
        self.text_box = QTextEdit()

        #create button for playing
        self.playBtn_1 = QPushButton()
        self.playBtn_1.setEnabled(False)
        self.playBtn_1.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn_1.clicked.connect(self.play_video_1)

        self.playBtn_2 = QPushButton()
        self.playBtn_2.setEnabled(False)
        self.playBtn_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn_2.clicked.connect(self.play_video_2)



        #create slider
        self.slider_1 = QSlider(Qt.Horizontal)
        self.slider_1.setRange(0,0)
        self.slider_1.sliderMoved.connect(self.set_position_1)

        self.slider_2 = QSlider(Qt.Horizontal)
        self.slider_2.setRange(0,0)
        self.slider_2.sliderMoved.connect(self.set_position_2)


        #create hbox layout
        hboxLayout_1 = QHBoxLayout()
        hboxLayout_1.setContentsMargins(0,0,0,0)

        hboxLayout_2 = QHBoxLayout()
        hboxLayout_2.setContentsMargins(0,0,0,0)

        #UI 排版
        hboxLayout_1.addWidget(openBtn_1)
        hboxLayout_1.addWidget(self.playBtn_1)
        hboxLayout_1.addWidget(self.slider_1)

        hboxLayout_2.addWidget(openBtn_2)
        hboxLayout_2.addWidget(self.playBtn_2)
        hboxLayout_2.addWidget(self.slider_2)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget_1)
        vboxLayout.addLayout(hboxLayout_1)
        vboxLayout.addWidget(videowidget_2)
        vboxLayout.addLayout(hboxLayout_2)

        vboxLayout_3 = QVBoxLayout()
        vboxLayout_3.addWidget(self.text_box)
        vboxLayout_3.addWidget(timeBtn)

        hboxLayout_all = QHBoxLayout()
        hboxLayout_all.setContentsMargins(0,0,0,0)
        hboxLayout_all.addLayout(vboxLayout)
        hboxLayout_all.addLayout(vboxLayout_3)

        self.setLayout(hboxLayout_all)

        self.mediaPlayer_1.setVideoOutput(videowidget_1)
        self.mediaPlayer_2.setVideoOutput(videowidget_2)

        #media player signals

        self.mediaPlayer_1.stateChanged.connect(self.mediastate_changed_1)
        self.mediaPlayer_1.positionChanged.connect(self.position_changed_1)
        self.mediaPlayer_1.durationChanged.connect(self.duration_changed_1)

        self.mediaPlayer_2.stateChanged.connect(self.mediastate_changed_2)
        self.mediaPlayer_2.positionChanged.connect(self.position_changed_2)
        self.mediaPlayer_2.durationChanged.connect(self.duration_changed_2)


    def open_file_1(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer_1.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn_1.setEnabled(True)
    def open_file_2(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video 2")

        if filename != '':
            self.mediaPlayer_2.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn_2.setEnabled(True)
    def input_time(self):
        t=self.text_box.toPlainText()
        self.mediaPlayer_1.setPosition(int(t))
    def play_video_1(self):
        if self.mediaPlayer_1.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer_1.pause()

        else:
            self.mediaPlayer_1.play()
    def play_video_2(self):
        if self.mediaPlayer_2.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer_2.pause()

        else:
            self.mediaPlayer_2.play()

    def mediastate_changed_1(self, state):
        if self.mediaPlayer_1.state() == QMediaPlayer.PlayingState:
            self.playBtn_1.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn_1.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )
    def mediastate_changed_2(self, state):
        if self.mediaPlayer_2.state() == QMediaPlayer.PlayingState:
            self.playBtn_2.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn_2.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed_1(self, position):
        self.slider_1.setValue(position)
    def position_changed_2(self, position):
        self.slider_2.setValue(position)

    def duration_changed_1(self, duration):
        self.slider_1.setRange(0, duration)
    def duration_changed_2(self, duration):
        self.slider_2.setRange(0, duration)

    def set_position_1(self, position):
        print(position)
        self.mediaPlayer_1.setPosition(position)
    def set_position_2(self, position):
        self.mediaPlayer_2.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())





app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())