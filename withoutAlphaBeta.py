import copy
import random
import sys

temp = sys.stdout


class WithoutAlphaBeta(object):
    def __init__(self):
        self.MAX = 3
        self.MIN = -3
        self.isRunning = False
        self.humanChess = None  # 记录玩家落子的位置(0-8),获取从主界面点击事件传来的数字(作为X玩家的落子位置)
        self.aiChess = 0  # 记录AI的落子位置,若AI先手，则默认落子于左上角(0位置)
        self.next_move = None  # 表示下一位玩家的身份
        self.aiFlag = None  # 当AI先手时置为1,从而直接落子于左上角,然后置为0,此后不再改变
        self.humanFlag = 0  # 表示主界面传入的X玩家落子位置是否合法,合法置为1,在主界面才允许添加对应棋子图片
        self.HUMAN = 1
        self.AI = 0
        self.depth = 1  # 代表第一层搜索

        # 设定获胜的组合方式(横、竖、斜)
        self.WIN_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                           (0, 3, 6), (1, 4, 7), (2, 5, 8),
                           (0, 4, 8), (2, 4, 6))

        # 设定棋盘按一行三个打印
        self.PRINTING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

        # 用一维列表表示棋盘:
        self.SLOTS = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        # self.SLOTS_ = ('左上', '上', '右上', '左', '中', '右', '左下', '下', '右下')

        # -1表示X玩家（YOU） 0表示空位 1表示O玩家(AI).
        self.X_token = -1
        self.Open_token = 0
        self.O_token = 1

        self.MARKERS = ['_', 'O', 'X']
        self.END_PHRASE = ('平局', '胜利', '必胜', '失败', '必败')

        self.init()

    def init(self):
        self.board = [self.Open_token for i in range(9)]
        self.result = 2
        # self.print_board(self.board)

    def valuation(self, board, player, next_player, depth=0):
        """极大极小值搜索当前局面分值"""
        ai_best = self.MIN
        player_best = self.MAX
        who_win = self.winner(board)
        '''若AI找到第一层能直接获胜的位置,则返回2'''
        if depth == 1 and self.legal_move_left(board):
            if who_win == self.O_token:
                return 2
            elif who_win == self.X_token:
                return -2
        else:
            if who_win != self.Open_token:
                # 有一方获胜（返回1:O玩家获胜 | 返回-1：X玩家获胜）
                return who_win
            elif not self.legal_move_left(board):
                # 没有空位,平局
                return 0
        # 检查当前玩家"player"的所有可落子点
        for move in self.SLOTS:
            if board[move] == self.Open_token:
                board[move] = player
                # 落子之后交换玩家，继续检验
                val = self.valuation(board, next_player, player)
                board[move] = self.Open_token
                if player == self.O_token:  # 当前玩家画圆圈O,是Max玩家(记号是1)
                    if val > ai_best:
                        ai_best = val
                else:  # 当前玩家画叉X,是Min玩家(记号是-1)
                    if val < player_best:
                        player_best = val
        if player == self.O_token:
            retval = ai_best
        else:
            retval = player_best
        return retval

    def winner(self, board):
        """ 判断局面的胜者,返回值-1表示X获胜,1表示O获胜,0表示平局或者未结束"""
        for triad in self.WIN_TRIADS:
            triad_sum = board[triad[0]] + board[triad[1]] + board[triad[2]]
            if triad_sum == 3 or triad_sum == -3:
                return board[triad[0]]  # 表示3个连续棋子的数值恰好也是-1:X,1:O
        return 0

    def legal_move_left(self, board):
        """ 判断棋盘上是否还有空位 """
        for slot in self.SLOTS:
            if board[slot] == self.Open_token:
                return True
        return False

    def print_board(self, board):
        """打印当前棋盘"""
        for row in self.PRINTING_TRIADS:
            r = ' '
            for hole in row:
                r += self.MARKERS[board[hole]] + ' '
            with open('outputlog.txt', 'a+') as f:
                sys.stdout = f
                print(r)
                sys.stdout = temp

    def determine_move(self, board):
        """
        决定电脑AI(玩家O)的下一步棋,
        若有绝杀优先选择，并强化对应玩家的得分：1+1 / -1-1
        若无,在估值相同的结果中随机选取步数
        """
        best_val = -3  # 本程序估值结果在[-2,-1,0,1,2]中
        ai_moves = []
        with open('outputlog.txt', 'a+') as f:
            sys.stdout = f
            print("AI开始思考")
            sys.stdout = temp
        for move in self.SLOTS:
            if board[move] == self.Open_token:
                board[move] = self.O_token
                val = self.valuation(board, self.X_token, self.O_token, self.depth)
                board[move] = self.Open_token
                with open('outputlog.txt', 'a+') as f:
                    sys.stdout = f
                    # move_ = self.SLOTS_[move]
                    print("AI如果下在", move + 1, ",将导致", self.END_PHRASE[val])
                    sys.stdout = temp
                if val > best_val:
                    best_val = val
                    ai_moves = [move]
                if val == best_val:
                    ai_moves.append(move)
        return random.choice(ai_moves)

    '''每一次玩家落子都会被调用，进行AI决策'''
    def game_start(self):
        # 开始下棋
        if self.legal_move_left(self.board) and self.winner(self.board) == self.Open_token:
            if self.next_move == self.HUMAN and self.legal_move_left(self.board):
                try:
                    humanmv = self.humanChess
                    if self.board[humanmv] != self.Open_token:
                        with open('outputlog.txt', 'a+') as f:
                            sys.stdout = f
                            print("此处无法落子，请重新选择落子位置！")
                            sys.stdout = temp
                        return
                    self.humanFlag = 1  # 代表此落子位置合法
                    self.board[humanmv] = self.X_token
                    # with open('outputlog.txt', 'a+') as f:
                    #     sys.stdout = f
                    #     print("\n玩家落子后：")
                    #     sys.stdout = temp
                    # self.print_board(self.board)
                    if (0 not in self.board) or (self.winner(self.board) != 0):  # 如果棋盘下满,或者提前分出胜负
                        self.game_over(self.board)
                        return
                    self.next_move = self.AI
                except:
                    pass
            if self.next_move == self.AI and self.legal_move_left(self.board):
                if self.aiFlag == 1:  # 只在AI先手时运行
                    self.ai_first_chess()
                    self.aiFlag = 0
                else:
                    aimv = self.determine_move(self.board)
                    with open('outputlog.txt', 'a+') as f:
                        sys.stdout = f
                        # move_ = self.SLOTS_[aimv]
                        print("\nAI最终决定下在", aimv + 1)
                        sys.stdout = temp
                    self.aiChess = aimv
                    self.board[aimv] = self.O_token
                    self.print_board(self.board)
                    if (0 not in self.board) or (self.winner(self.board) != 0):
                        self.game_over(self.board)
                        return
                    self.next_move = self.HUMAN

    def game_over(self, board):
        # 输出结果
        with open('outputlog.txt', 'a+') as f:
            sys.stdout = f
            print("\n最终棋盘如下：")
            sys.stdout = temp
        self.print_board(board)
        with open('outputlog.txt', 'a+') as f:
            sys.stdout = f
            print("最终结果为：" + ["平局", "AI赢了", "你赢了"][self.winner(board)])
            sys.stdout = temp
        self.result = self.winner(board)

    '''设置先后手'''
    def set_order(self, order):
        self.next_move = order
        if self.next_move == 0:  # 当AI先手时
            self.aiFlag = 1

    def ai_first_chess(self):
        aimv = self.aiChess
        with open('outputlog.txt', 'a+') as f:
            sys.stdout = f
            # move_ = self.SLOTS_[aimv]
            print("AI决定下在", aimv + 1)
            sys.stdout = temp
        self.board[aimv] = self.O_token
        self.next_move = self.HUMAN
        self.print_board(self.board)

    '''获取玩家的落子位置'''
    def get_human_position(self, position):
        self.humanChess = position

    '''获取AI落子的位置'''
    def get_ai_position(self):
        return self.aiChess
