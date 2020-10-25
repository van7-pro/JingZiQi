from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QScrollArea, QScrollBar
from PyQt5.QtGui import QFont, QTextCursor, QTextOption
from PyQt5.QtCore import Qt


class StrategyWidget(QWidget):
    def __init__(self, width, height, gameLogic_1, parent=None):
        super(QWidget, StrategyWidget).__init__(self, parent)
        self.fixedWidth = width
        self.fixedHeight = height
        self.gameLogic_1 = gameLogic_1
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.fixedWidth, self.fixedHeight)
        gameStrategyLabel = QLabel("AI决策过程", self)
        gameStrategyLabel.move(80, 15)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)  # 设置加粗类型
        font.setPointSize(20)  # 设置字体大小
        font.setWeight(30)  # 设置字体粗细
        gameStrategyLabel.setFont(font)

        showHint = QLabel("棋盘范围内单击可刷新下方决策过程！", self)
        showHint.move(23, 40)
        showHint.resize(320, 75)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)  # 设置加粗类型
        font.setPointSize(12)  # 设置字体大小
        font.setWeight(30)  # 设置字体粗细
        showHint.setFont(font)

        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(240)  # 设置换行的固定宽度，即350个像素为一行，若该长度超出了窗口的长度，那么会产生一个水平的滚动条
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)  # 按像素限制换行
        self.process.setFixedWidth(260)
        # self.process.setWordWrapMode(QTextOption.WordWrap)  # 软换行
        self.process.setFixedHeight(370)
        self.process.move(23, 110)

        # self.process.setVerticalScrollBarPolicy(2)

    '''读取txt文件的内容并显示'''
    def refeshStrategyMessage(self, flag=0):
        if flag == 1:
            try:
                with open('outputlog.txt', 'r+') as f:
                    msg = f.read()
                    self.process.setPlainText(msg)
                    self.process.moveCursor(QTextCursor.End)  # 将滚动条固定至底部
            except:
                pass
