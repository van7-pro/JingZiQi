from PyQt5.QtWidgets import QLabel, QDialog, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


class ChooseAlgorithmWindow(QDialog):
    alphaBetaSignal = pyqtSignal()
    maxMinSignal = pyqtSignal()

    def __init__(self, width, height, parent, listener):
        super(QDialog, ChooseAlgorithmWindow).__init__(self, parent)
        self.setFixedSize(width, height)

        self.alphaBetaSignal.connect(listener.alphaBetaLogic)
        self.maxMinSignal.connect(listener.maxMinLogic)

        chooseLabel = QLabel("请选择AI算法", self)
        chooseLabel.setFixedSize(450, 200)
        chooseLabel.move(80, 0)

        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(30)   # 设置字体大小
        font.setWeight(80)      # 设置字体粗细
        chooseLabel.setFont(font)
        chooseLabel.setStyleSheet("color: green")

        font.setPointSize(12)

        firstButton = QPushButton("极大极小算法\n+ab剪枝", self)
        firstButton.setFixedSize(120, 50)
        firstButton.move(70, 200)
        firstButton.setFont(font)
        firstButton.setStyleSheet("background-color:black;color:white;")
        firstButton.clicked.connect(self.firstButtonEvent)

        secondButton = QPushButton("极大极小算法", self)
        secondButton.setFixedSize(120, 50)
        secondButton.move(240, 200)
        secondButton.setFont(font)
        secondButton.setStyleSheet("background-color:white;color:black;")
        secondButton.clicked.connect(self.secondButtonEvent)

        self.setStyleSheet("background-color:rgb(245, 245, 220)")
        # self.setStyleSheet("background-color:gray")
        self.setWindowTitle("AI算法选择")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def firstButtonEvent(self):
        self.alphaBetaSignal.emit()
        self.close()

    def secondButtonEvent(self):
        self.maxMinSignal.emit()
        self.close()
