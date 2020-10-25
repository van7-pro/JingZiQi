from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QPushButton, QLabel
from PyQt5.QtGui import QPen, QIcon, QPainter, QBrush, QColor, QPalette, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import base64

# from boardBackground_png import img as board
# tmp = open('board.jpg', 'wb')        # 创建临时的文件
# tmp.write(base64.b64decode(board))    # 把这个one图片解码出来，写入文件中去。
# tmp.close()


class ChessBoardGui(QWidget):
    putChessCheck = pyqtSignal()

    # def __init__(self, parent, gameLogit):
    def __init__(self, parent):
        super(QWidget, ChessBoardGui).__init__(self, parent)
        """Chess Board Init"""
        self.lineWidth = 10
        self.lineInterval = 120
        self.chessBoardTopLeftPos = (50, 50)
        self.preparedChess = None
        self.point = None
        # self.currentPlayer = 0
        # self.chessArray = np.zeros([15, 15], dtype=int)
        # self.gameLogit = gameLogit
        self.gameRunning = False
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.setAutoFillBackground(True)
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('/home/wangqi/桌面/JinZiQi/figures/boardBackground.png')))
        # palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('board.jpg')))
        # palette1.setColor(QPalette.Background, QColor(245, 245, 220))
        self.setPalette(palette1)

    def setGameStatus(self, status):
        self.gameRunning = status

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawChessBoard(qp)
        qp.end()

    def drawChessBoard(self, qp):
        chessBoardWidth = 3 * (self.lineInterval + self.lineWidth)
        pen = QPen(Qt.black, self.lineWidth, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(2):  # 画横线
            startX = self.chessBoardTopLeftPos[0]
            startY = self.chessBoardTopLeftPos[1] + (i + 1) * (self.lineWidth + self.lineInterval)
            qp.drawLine(startX, startY, startX + chessBoardWidth, startY)

        for i in range(2):  # 画竖线
            startX = self.chessBoardTopLeftPos[0] + (i + 1) * (self.lineWidth + self.lineInterval)
            startY = self.chessBoardTopLeftPos[1]
            qp.drawLine(startX, startY, startX, startY + chessBoardWidth)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = QWidget()
#     ChessBoardGui(w)
#     w.show()
#     app.exit(app.exec_())
