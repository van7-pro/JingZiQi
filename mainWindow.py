from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QLabel, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, QCoreApplication
import os
import sys
import base64

from startWindow import startWidget
from boardWindow import ChessBoardGui
from strategyWindow import StrategyWidget
from chooseOrderWindow import ChooseOrderWindow
from gamePlay_new import GameLogic
from withoutAlphaBeta import WithoutAlphaBeta
from gameOverWindow import GameOverWindow
from chooseAlgorithmWindow import ChooseAlgorithmWindow

# from circle_png import img as circle
# from cross_png import img as cross
# from gameIcon_jpg import img as icon

# tmp = open('icon.jpg', 'wb')        # 创建临时的文件
# tmp.write(base64.b64decode(icon))    # 把这个one图片解码出来，写入文件中去。
# tmp.close()
# tmp = open('circle.jpg', 'wb')        # 创建临时的文件
# tmp.write(base64.b64decode(circle))    # 把这个one图片解码出来，写入文件中去。
# tmp.close()
# tmp = open('cross.jpg', 'wb')        # 创建临时的文件
# tmp.write(base64.b64decode(cross))    # 把这个one图片解码出来，写入文件中去。
# tmp.close()


class MainWindow(QMainWindow):
    gameOverSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.windowWeight = 1000
        self.windowHeight = 500

        """主窗口"""
        self.setFixedSize(self.windowWeight, self.windowHeight)
        self.setWindowIcon(QIcon('/home/wangqi/桌面/JinZiQi/figures/gameIcon.jpg'))
        # self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("井字棋AI")

        self.initUI()
        self.center()
        self.show()

        self.Png1 = QPixmap('/home/wangqi/桌面/JinZiQi/figures/circle.png')
        self.Png2 = QPixmap('/home/wangqi/桌面/JinZiQi/figures/cross.png')
        # self.Png1 = QPixmap('circle.jpg')
        # self.Png2 = QPixmap('cross.jpg')

        self.gameOverSignal.connect(self.gameOverEvent)
        self.gameOverClickedMark = False

    def initUI(self):
        self.gameLogic = GameLogic()
        self.gameStarted = False
        self.gameRunning = False
        self.algorithm = 1  # 算法选择的标志位

        # self.changeAlgorithm()

        """具体的实现功能的窗口"""
        self.mainWidget = QWidget()

        infoWidget_ = QWidget(self.mainWidget)  # 输出决策信息的区域
        self.infoWidget = StrategyWidget(300, 500, self.gameLogic, infoWidget_)
        self.infoWidget.move(0, 0)
        # infoWidget.setFixedSize(300, 500)

        self.boardWidget = QWidget(self.mainWidget)  # 绘制棋盘的区域
        self.boardWidget.setFixedSize(500, 500)
        self.boardWidget.move(300, 0)

        startWidget_ = QWidget(self.mainWidget)  # 绘制开始游戏、新游戏等按钮的区域
        self.startGUI = startWidget(180, 500, self.gameLogic, startWidget_)
        self.startGUI.move(830, 0)
        self.startGUI.exitGameButtonClicked.connect(self.exitGameEvent)

        self.setCentralWidget(self.mainWidget)  # 设置中心组件，缺少此行将导致自定义的窗口无法在主窗口中正确显示

        self.chessBoardGui = ChessBoardGui(self.boardWidget)  # 绘制棋盘

        # 开始等按钮的GUI
        # self.startGUI = startWidget(180, 500, self.gameLogic_1, startWidget_)
        self.startGUI.startPauseButtonClicked.connect(self.startPauseEvent)  # 接收消息
        self.startGUI.algoChooseButtonClicked.connect(self.algoChooseEvent)
        self.startGUI.newGameButtonClicked.connect(self.newGameEvent)
        self.startGUI.exitGameButtonClicked.connect(self.exitGameEvent)

        # self.showImg(43, 43, Png1)
        """没人比我更懂暴力"""
        self.img0 = QLabel(self.boardWidget)
        self.img1 = QLabel(self.boardWidget)
        self.img2 = QLabel(self.boardWidget)
        self.img3 = QLabel(self.boardWidget)
        self.img4 = QLabel(self.boardWidget)
        self.img5 = QLabel(self.boardWidget)
        self.img6 = QLabel(self.boardWidget)
        self.img7 = QLabel(self.boardWidget)
        self.img8 = QLabel(self.boardWidget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    '''玩家先手'''
    def firstOrderEvent(self):
        self.gameStarted = True
        self.gameLogic.isRunning = True
        self.startGUI.changeStartButtonInfo()
        self.startGUI.updatePlayerInfo("先手", "后手")
        self.gameLogic.set_order(1)
        self.startPauseEvent()

    '''AI先手'''
    def secondOrderEvent(self):
        self.gameStarted = True
        self.gameLogic.isRunning = True
        self.startGUI.changeStartButtonInfo()
        self.startGUI.updatePlayerInfo("后手", "先手")
        self.gameLogic.set_order(0)
        self.showImg0(self.Png1)  # AI先手时,默认落子在左上角(0位置)
        self.gameLogic.game_start()
        self.startPauseEvent()

    def changeAlgorithm(self):
        if self.algorithm == 1:
            self.gameLogic = GameLogic()
        elif self.algorithm == 2:
            self.gameLogic = WithoutAlphaBeta()

    def startPauseEvent(self):
        if not self.gameStarted:
            ChooseOrderWindow(400, 300, self.mainWidget, self)
        else:
            if self.gameRunning:
                self.chessBoardGui.setGameStatus(False)
                # self.startGUI.stopGameTimer()
            else:
                self.chessBoardGui.setGameStatus(True)
                # self.startGUI.startGameTimer()
            self.gameRunning = not self.gameRunning

    def algoChooseEvent(self):
        if not self.gameStarted:
            ChooseAlgorithmWindow(400, 300, self.mainWidget, self)

    def alphaBetaLogic(self):
        self.algorithm = 1
        self.changeAlgorithm()
        self.startGUI.updateAlgoInfo("极大极小算法\n+ab剪枝")

    def maxMinLogic(self):
        self.algorithm = 2
        self.changeAlgorithm()
        self.startGUI.updateAlgoInfo("极大极小算法")

    '''根据设置的标志位来区分添加哪一方的棋子图片,pix1 pix2:坐标, png:显示的图像'''
    def showImg0(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img0.setGeometry(55, 50, 115, 115)
        self.img0.setPixmap(png)
        self.img0.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg1(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img1.setGeometry(188, 50, 115, 115)
        self.img1.setPixmap(png)
        self.img1.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg2(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img2.setGeometry(320, 50, 115, 115)
        self.img2.setPixmap(png)
        self.img2.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg3(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img3.setGeometry(55, 188, 115, 115)
        self.img3.setPixmap(png)
        self.img3.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg4(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img4.setGeometry(188, 188, 115, 115)
        self.img4.setPixmap(png)
        self.img4.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg5(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img5.setGeometry(320, 188, 115, 115)
        self.img5.setPixmap(png)
        self.img5.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg6(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img6.setGeometry(55, 320, 115, 115)
        self.img6.setPixmap(png)
        self.img6.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg7(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img7.setGeometry(188, 320, 115, 115)
        self.img7.setPixmap(png)
        self.img7.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showImg8(self, png):
        # self.img = QLabel(self.boardWidget)
        self.img8.setGeometry(320, 320, 115, 115)
        self.img8.setPixmap(png)
        self.img8.setScaledContents(True)  # 图片自适应窗口部件的尺寸

    def showAiChess(self, position):
        if position == 0:
            self.showImg0(self.Png1)
        elif position == 1:
            self.showImg1(self.Png1)
        elif position == 2:
            self.showImg2(self.Png1)
        elif position == 3:
            self.showImg3(self.Png1)
        elif position == 4:
            self.showImg4(self.Png1)
        elif position == 5:
            self.showImg5(self.Png1)
        elif position == 6:
            self.showImg6(self.Png1)
        elif position == 7:
            self.showImg7(self.Png1)
        elif position == 8:
            self.showImg8(self.Png1)

    def newGameEvent(self):
        self.gameLogic.isRunning = False
        self.initUI()
        self.gameLogic.init()

    def exitGameEvent(self):
        self.gameLogic.isRunning = False
        QCoreApplication.instance().quit()

    def gameOverEvent(self):
        # self.infoGUI.stopGameTimer()
        # print(self.gameLogic.result)
        self.gameOverClickMark = False
        GameOverWindow(400, 300, self.mainWidget, self.gameLogic.result, self)
        if not self.gameOverClickMark:
            self.newGameEvent()

    def putChessEvent(self):
        winner = self.gameLogic.result
        if winner != 2:
            self.gameOverSignal.emit()

    def closeEvent(self, e):
        self.exitGameEvent()

    '''重定义鼠标单击事件,单击棋盘内区域刷新决策框'''
    def mousePressEvent(self, e):
        # print(e.localPos().x(), e.localPos().y())  # 返回鼠标相对于该窗口的坐标位置
        if (350 < e.localPos().x() < 750) and (60 < e.localPos().y() < 450):
            self.infoWidget.refeshStrategyMessage(flag=1)

    '''重定义鼠标双击事件,双击棋盘内对应区域进行位置判定和正确棋子图片添加的操作'''
    def mouseDoubleClickEvent(self, e):
        if not self.gameRunning:
            return
        # print(e.localPos().x(), e.localPos().y())  # 返回鼠标相对于该窗口的坐标位置
        '''将玩家落子的位置传入游戏中'''
        if (360 < e.localPos().x() < 460) and (70 < e.localPos().y() < 160):
            self.cleanLog()  # 每次落子前清理上一次的输出日志,由于决策信息的文本框滚动条出现无法滚动的问题,无奈之举
            self.gameLogic.get_human_position(0)  # 向算法传入玩家落子的位置(0-8)
            self.gameLogic.game_start()  # 开始游戏
            if self.gameLogic.humanFlag == 1:  # 位置合法才可以落子
                self.showImg0(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)  # 显示AI的落子位置
            self.putChessEvent()
        if (500 < e.localPos().x() < 600) and (70 < e.localPos().y() < 160):
            self.cleanLog()
            self.gameLogic.get_human_position(1)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg1(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (640 < e.localPos().x() < 740) and (70 < e.localPos().y() < 160):
            self.cleanLog()
            self.gameLogic.get_human_position(2)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg2(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (360 < e.localPos().x() < 460) and (200 < e.localPos().y() < 290):
            self.cleanLog()
            self.gameLogic.get_human_position(3)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg3(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (500 < e.localPos().x() < 600) and (200 < e.localPos().y() < 290):
            self.cleanLog()
            self.gameLogic.get_human_position(4)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg4(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (640 < e.localPos().x() < 740) and (200 < e.localPos().y() < 290):
            self.cleanLog()
            self.gameLogic.get_human_position(5)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg5(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (360 < e.localPos().x() < 460) and (350 < e.localPos().y() < 440):
            self.cleanLog()
            self.gameLogic.get_human_position(6)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg6(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (500 < e.localPos().x() < 600) and (350 < e.localPos().y() < 440):
            self.cleanLog()
            self.gameLogic.get_human_position(7)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg7(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()
        if (640 < e.localPos().x() < 740) and (350 < e.localPos().y() < 440):
            self.cleanLog()
            self.gameLogic.get_human_position(8)
            self.gameLogic.game_start()
            if self.gameLogic.humanFlag == 1:
                self.showImg8(self.Png2)
            self.showAiChess(self.gameLogic.aiChess)
            self.putChessEvent()

    def cleanLog(self):
        if os.path.exists('outputlog.txt'):
            os.remove('outputlog.txt')

    # def wheelEvent(self, e):
    #     pass


if __name__ == '__main__':
    if os.path.exists('outputlog.txt'):
        os.remove('outputlog.txt')
    app = QApplication(sys.argv)
    window = MainWindow()
    # os.remove('icon.jpg')  # 用完可以删除这个临时图片
    # os.remove('cross.jpg')
    # os.remove('circle.jpg')
    # os.remove('board.jpg')
    sys.exit(app.exec_())
