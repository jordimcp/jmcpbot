import berserk
import threading
import chess.pgn
from board import *
from test import *
import pickle
import chess


class Bot():
    def __init__(self, bot_id, color):
        self.id = bot_id
        self.color = color[0]
        mygames_filename = "jmcpgeh_winning_fen.pkl"
        jmcp_file = open(mygames_filename, "rb")
        self.jmcp_games = pickle.load(jmcp_file)
        jmcp_file.close()
        self.board = Board(self.color[0])
        self.turn = 0  # debug
        self.tmp_board = chess.Board()

    def get_color(self):
        return self.color

    def get_id(self):
        return self.id

    def start_game(self):
        self.board.init_board()
        self.turn = 0

    def board_from_fen(self, fen):
        board = []
        for i in range(8):
            board.append(['·', '·', '·', '·', '·', '·', '·', '·'])
        row = 0
        col = 0
        for c in fen:
            if c == '/':
                row += 1
                col = 0
            elif c.isdigit():
                col += int(c)
            elif c == ' ':
                break
            else:
                board[row][col] = c
                col += 1
        for i in range(8):
            print(board[i])
        return board

    def move_from_boards(self, curr_b, next_b):
        row_o = 0
        col_o = 0
        row_d = 0
        col_d = 0
        for row in range(8):
            for col in range(8):
                if curr_b[row][col] != next_b[row][col]:
                    print(curr_b[row][col], 'to', next_b[row][col])
                    if next_b[row][col] == '·':
                        row_o = row
                        col_o = col
                        print('Move from', row, col)
                    else:
                        row_d = row
                        col_d = col
                        print('Move to', row, col)
        return [7-row_o, col_o, 7-row_d, col_d]

    def extract_move_from_game(self, game, fen):
        n_move = 0
        for m in game:
            n_move += 1
            if fen == m:
                break
        print("Current position", game[n_move-1])
        print("Fen to extract from", game[n_move])
        curr_board = self.board_from_fen(game[n_move-1])
        print("\n\n")
        next_board = self.board_from_fen(game[n_move])
        move = self.move_from_boards(curr_board, next_board)
        return move

    def from_jmcp(self, opponent_move):
        col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        row = [1, 2, 3, 4, 5, 6, 7, 8]
        found = False
        self.tmp_board.push(chess.Move.from_uci(opponent_move))
        fen = self.tmp_board.fen()
        self.board_from_fen(fen)
        ngame = 0
        fgame = 0
        if self.color == 'b':
            for game in self.jmcp_games:
                ngame += 1
                for key in game:
                    if key == '0-1':
                        if fen in game[key]:
                            fgame += 1
                            print("Have position in some game")
                            move = self.extract_move_from_game(game[key], fen)
                            print("Resulting move", move)
                            found = True
            print("Game Looked: ",ngame,"(",fgame,")","-",len(self.jmcp_games))
            if found:
                c_o = col[move[1]]
                r_o = str(row[move[0]])
                c_f = col[move[3]]
                r_f = str(row[move[2]])
                bot_move = c_o+r_o+c_f+r_f
                print("Bot move => ",bot_move)
                legal = self.board.is_legal(bot_move)
                self.board.update_board(bot_move)
                self.tmp_board.push(chess.Move.from_uci(bot_move))
            else:
                bot_move = self.move_whatever_legal(opponent_move)
        return bot_move

    def move_whatever_legal(self, opponent_move):
        col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        row = [1, 2, 3, 4, 5, 6, 7, 8]
        # f = open("debug/black_moves.txt","r")
        # result = f.read()
        # moves = result.split("\n")
        # bot_move = "move"
        # if self.turn >= len(moves)-1:
        #  print("Game FINISHED no more moves")
        # else:
        # bot_move = moves[self.turn]
        # print("Black moves", bot_move)
        # self.turn += 1
        legal = False
        # legal = self.board.is_legal(bot_move)
        for c in range(8):
            for r in range(8):
                c_o = col[c]
                r_o = str(row[r])
                for i in range(8):
                    for k in range(8):
                        c_f = col[i]
                        r_f = str(row[k])
                        bot_move = c_o+r_o+c_f+r_f
                        legal = self.board.is_legal(bot_move)
                        if legal:
                            break
                    if legal:
                        break
                if legal:
                    break
            if legal:
                break
        if legal:
            print(bot_move)
            self.board.update_board(bot_move)
            # f.close()
        else:
            print("Move not legal")
            self.board.debug_msg("********************")
            self.board.debug_msg(
                ("ERROR:TURN NOT LEGAL (move was: %s)") % (bot_move))
            self.board.debug_msg("********************")
            # assert( 1 == 0)
        return bot_move

    def make_decision(self, opponent_move):
        self.board.set_opponent_move(opponent_move)
        self.board.update_board(opponent_move)
        #bot_move = self.move_whatever_legal(opponent_move)
        bot_move = self.from_jmcp(opponent_move)
        return bot_move


# Debug

# def setup_next_game(bot):
#   bot.start_game()
#   f=open("debug/white_moves.txt","r")
#   result = f.read()
#   moves = result.split("\n")[:-1]
#   f.close()
#   return moves
# while True:
#   bot = Bot('BOT','black')
#   test = Test("/home/joma/pers/jmcpbot/databases/lichess_jmcpgeh_2021-01-06.pgn")
#   test.create_move_files()
#   total_games = 1000
#   for i in range(total_games):
#     moves = setup_next_game(bot)
#     for m in moves:
#       print("White moves:", m)
#       bot.make_decision(m)
#     test.next_game()
#     if i < total_games-1:
#       test.create_move_files()
#   break
