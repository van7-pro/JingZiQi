from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
from gamePlay_new import *
import os


class startWidget(QWidget):
    startPauseButtonClicked = pyqtSignal()
    newGameButtonClicked = pyqtSignal()
    exitGameButtonClicked = pyqtSignal()
    algoChooseButtonClicked = pyqtSignal()

    def __init__(self, width, height, gameLogic, parent=None):
        super(QWidget, startWidget).__init__(self, parent)
        self.fixedWidth = width
        self.fixedHeight = height
        self.gameRunning = False
        self.gameLogic = gameLogic
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.fixedWidth, self.fixedHeight)

        """Player info"""
        self.playerInfoLable = QLabel("玩家 \t{:}\nAI \t{:}".format("", ""), self)
        self.playerInfoLable.setFixedSize(self.fixedWidth, 70)
        self.playerInfoLable.move(0, 14)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)  # 设置加粗类型
        font.setPointSize(18)  # 设置字体大小
        font.setWeight(35)  # 设置字体粗细
        self.playerInfoLable.setFont(font)

        """Algorithm info"""
        self.AlgoInfoLable = QLabel("当前AI算法为：\n{:}".format("极大极小算法\n+ab剪枝"), self)
        self.AlgoInfoLable.setFixedSize(self.fixedWidth, 100)
        self.AlgoInfoLable.move(0, 85)
        font.setBold(True)  # 设置加粗类型
        font.setPointSize(15)  # 设置字体大小
        font.setWeight(35)  # 设置字体粗细
        self.AlgoInfoLable.setFont(font)

        font.setPointSize(20)  # 设置字体大小
        """Start and pause button"""
        self.startPauseButton = QPushButton("开始游戏", self)
        self.startPauseButton.move(0, 190)
        self.startPauseButton.setFixedSize(150, 60)
        self.startPauseButton.setFont(font)
        # self.startPauseButton.setFlat(True)
        self.startPauseButton.setAutoFillBackground(True)
        self.startPauseButton.setStyleSheet("background-color:rgb(171,198,219);")
        self.startPauseButton.clicked.connect(self.startPauseButtonClickedEvent)

        self.chooseAlgoButton = QPushButton("选择AI算法", self)
        self.chooseAlgoButton.move(0, 260)
        self.chooseAlgoButton.setFixedSize(150, 60)
        self.chooseAlgoButton.setFont(font)
        # self.chooseAlgoButton.setFlat(True)
        self.chooseAlgoButton.setAutoFillBackground(True)
        self.chooseAlgoButton.setStyleSheet("background-color:rgb(123,157,192);")
        self.chooseAlgoButton.clicked.connect(self.algoChooseButtonClickedEvent)

        """New game button"""
        self.newGameButton = QPushButton("新游戏", self)
        self.newGameButton.move(0, 330)
        self.newGameButton.setFixedSize(150, 60)
        self.newGameButton.setFont(font)
        self.newGameButton.setAutoFillBackground(True)
        self.newGameButton.setStyleSheet("background-color:rgb(255,210,189);")
        self.newGameButton.clicked.connect(self.newGameButtonClickedEvent)

        """Exit game button"""
        self.exitGameButton = QPushButton("退出游戏", self)
        self.exitGameButton.move(0, 400)
        self.exitGameButton.setFixedSize(150, 60)
        self.exitGameButton.setFont(font)
        self.exitGameButton.setAutoFillBackground(True)
        self.exitGameButton.setStyleSheet("background-color:rgb(236, 162,153);")
        self.exitGameButton.clicked.connect(self.exitGameButtonClickedEvent)

    def updatePlayerInfo(self, s1, s2):
        self.playerInfoLable.setText("玩家:\t{:}\nAI:\t{:}".format(s1, s2))

    def updateAlgoInfo(self, s):
        self.AlgoInfoLable.setText("当前AI算法为：\n{:}".format(s))

    def changeStartButtonInfo(self):
        if not self.gameRunning:
            self.gameRunning = True
            self.startPauseButton.setText("暂停游戏")
        else:
            self.gameRunning = False
            self.startPauseButton.setText("继续游戏")

    def startPauseButtonClickedEvent(self):
        if self.gameLogic.isRunning:
            self.changeStartButtonInfo()
            self.startPauseButtonClicked.emit()
        else:
            self.startPauseButtonClicked.emit()

    def algoChooseButtonClickedEvent(self):
        if self.gameLogic.isRunning:
            pass
        else:
            self.algoChooseButtonClicked.emit()

    def newGameButtonClickedEvent(self):
        if os.path.exists('outputlog.txt'):
            os.remove('outputlog.txt')
        self.newGameButtonClicked.emit()

    def exitGameButtonClickedEvent(self):
        self.exitGameButtonClicked.emit()
