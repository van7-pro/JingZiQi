from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
import os


class GameOverWindow(QDialog):
    newGameSignal = pyqtSignal()

    def __init__(self, width, height, parent, winner, listener):
        super(QDialog, GameOverWindow).__init__(self, parent)
        self.setFixedSize(width, height)
        self.listener = listener

        self.newGameSignal.connect(listener.newGameEvent)

        # print(winner)
        """Game over label"""
        if winner == 0:
            gameOverLabel = QLabel("平局!", self)
            gameOverLabel.setFixedSize(width, 200)
            gameOverLabel.move(150, 0)
        elif winner == -1:
            gameOverLabel = QLabel("玩家获胜!", self)
            gameOverLabel.setFixedSize(width, 200)
            gameOverLabel.move(100, 0)
        elif winner == 1:
            gameOverLabel = QLabel("AI获胜!", self)
            gameOverLabel.setFixedSize(width, 200)
            gameOverLabel.move(120, 0)
        else:
            raise Exception("Game over window error!")

        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(40)   # 设置字体大小
        font.setWeight(80)      # 设置字体粗细
        gameOverLabel.setFont(font)
        gameOverLabel.setStyleSheet("color: red")

        # if winner == 1 or winner == 0:

        font.setPointSize(20)

        newGameButton = QPushButton("结束游戏", self)
        newGameButton.setFixedSize(150, 80)
        newGameButton.move(125, 180)
        newGameButton.setFont(font)
        newGameButton.setStyleSheet("background-color:white;color:black;")
        newGameButton.clicked.connect(self.newGameButtonEvent)

        self.setStyleSheet("background-color:rgb(245, 245, 220)")
        self.setWindowTitle("游戏结束")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def newGameButtonEvent(self):
        self.listener.gameOverClickMark = True
        self.newGameSignal.emit()
        if os.path.exists('outputlog.txt'):
            os.remove('outputlog.txt')
        # self.listener.infoGUI.startGameTimer()
        # self.listener.infoGUI.resetGameTimer()
        # self.listener.gameLogic.isRunning = True
        self.listener.gameLogic.isRunning = False
        self.close()
