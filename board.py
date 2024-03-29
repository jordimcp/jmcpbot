import berserk
import threading
import chess.pgn
from piece import *
from pawn import *
from bishop import *
from rook import *
from queen import *
from king import *
from knight import *
from empty import *
import copy


class Board():
    def __init__(self, bot_color):
        self.bot_color = bot_color
        self.n_game = 0
        self.column = {'a': 0, 'b': 1, 'c': 2,
                       'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self.position = []
        self.moves = 0
        self.init_board()
        self.opponent_move = []
        self.short_castle_allowed = True
        self.long_castle_allowed = True

    def debug_msg(self, txt):
        f = open(self.filename, "a", newline='')
        f.write(txt + "\n")
        f.close()

    def init_board(self):
        self.position = []
        self.moves = 0
        self.filename = ("debug/debug_position%s.txt") % (self.n_game)
        self.n_game += 1
        f = open(self.filename, "w", newline='')
        white_pawns = []
        black_pawns = []
        dummy_pawns = []
        dummy_black_pawns = []
        emptys = []
        for i in range(8):
            pawn = Pawn('w', [1, i])
            white_pawns.append(pawn)
        for i in range(8):
            piece = Pawn('w', [0, i])
            if (i == 1) or (i == 6):
                piece = Knight('w', [0, i])
            if (i == 2) or (i == 5):
                piece = Bishop('w', [0, i])
            if (i == 0) or (i == 7):
                piece = Rook('w', [0, i])
            if (i == 3):
                piece = Queen('w', [0, i])
            if (i == 4):
                piece = King('w', [0, i])
                white_king_pos = [0, i]
            dummy_pawns.append(piece)
        for i in range(8):
            pawn = Pawn('b', [6, i])
            black_pawns.append(pawn)
        for i in range(8):
            piece = Pawn('b', [7, i])
            if (i == 1) or (i == 6):
                piece = Knight('b', [7, i])
            if (i == 2) or (i == 5):
                piece = Bishop('b', [7, i])
            if (i == 0) or (i == 7):
                piece = Rook('b', [7, i])
            if (i == 3):
                piece = Queen('b', [7, i])
            if (i == 4):
                piece = King('b', [7, i])
                black_king_pos = [7, i]
            dummy_black_pawns.append(piece)
        self.position.append(dummy_pawns)
        self.position.append(white_pawns)
        for i in range(8):
            empty_box = Empty('None', [2, i])
            emptys.append(empty_box)
        self.position.append(emptys)
        emptys = []
        for i in range(8):
            empty_box = Empty('None', [3, i])
            emptys.append(empty_box)
        self.position.append(emptys)
        emptys = []
        for i in range(8):
            empty_box = Empty('None', [4, i])
            emptys.append(empty_box)
        self.position.append(emptys)
        emptys = []
        for i in range(8):
            empty_box = Empty('None', [5, i])
            emptys.append(empty_box)
        self.position.append(emptys)
        self.position.append(black_pawns)
        self.position.append(dummy_black_pawns)
        if self.bot_color == 'w':
            self.king_pos = white_king_pos
        else:
            self.king_pos = black_king_pos

    def print_board(self, move):
        f = open(self.filename, "a", newline='')
        f.write("\n")
        self.moves += 1
        f.write(("Move %d: %s\n") % (self.moves, move))
        for r in range(8):
            for c in range(8):
                piece = self.position[r][c]
                if piece.name != "Empty":
                    # print(self.position[r][c].color+self.position[r][c].name[0],end='|')
                    f.write(self.position[r][c].color +
                            self.position[r][c].name[0] + '|')
                else:
                    #print("  ",end='|')
                    f.write("  "'|')
            #print(" ")
            f.write("  \n")
            for i in range(8):
                # print("--",end='|')
                f.write("--"'|')
            #print(" ")
            f.write("  \n")
        f.close()

    def print_potential_board(self, position):
        f = open(self.filename, "a", newline='')
        f.write("\n")
        for r in range(8):
            for c in range(8):
                piece = position[r][c]
                if piece.name != "Empty":
                    f.write(position[r][c].color+position[r][c].name[0] + '|')
                else:
                    f.write("  "'|')
            f.write("  \n")
            for i in range(8):
                f.write("**"'*')
            f.write("  \n")
        f.close()

    def set_opponent_move(self, opponent_move):
        self.opponent_move = self.decode_move(opponent_move)

    def decode_move(self, move):
        c_orig = self.column[move[0]]
        r_orig = int(move[1])-1
        c_dest = self.column[move[2]]
        r_dest = int(move[3])-1
        return [r_orig, c_orig, r_dest, c_dest]

    def is_legal(self, move):
        move_d = self.decode_move(move)
        if len(move) > 4:  # TODO: Check if legal
            legal = True
            promot = move[4]
        else:
            legal = self.is_legal_move(move_d)
        return legal

    def update_board(self, move):
        print("Updating board..")
        move_d = self.decode_move(move)
        piece = self.position[move_d[0]][move_d[1]]
        togo = self.position[move_d[2]][move_d[3]]
        if len(move) > 4:
            print("Promotion!!!!!!")
            self.debug_msg("Pawn being promoted")
            empty = Empty('None', move_d[0:2])
            self.position[move_d[0]][move_d[1]] = empty
            if move[4] == 'q':
                self.position[move_d[2]][move_d[3]] = Queen(
                    piece.color, [move_d[2], move_d[3]])
            elif move[4] == 'b':
                self.position[move_d[2]][move_d[3]] = Bishop(
                    piece.color, [move_d[2], move_d[3]])
            elif move[4] == 'n':
                self.position[move_d[2]][move_d[3]] = Knight(
                    piece.color, [move_d[2], move_d[3]])
            elif move[4] == 'r':
                self.position[move_d[2]][move_d[3]] = Rook(
                    piece.color, [move_d[2], move_d[3]])
        else:
            piece.move(move_d)
            # Updating position of our king
            if piece.name == 'King' and piece.color == self.bot_color:
                self.king_pos = move_d[2:]
            # Castle
            if (piece.name == 'King') and (togo.name == 'Rook'):
                # if (piece.name == 'King') and abs(move_d[1] - move_d[3]) == 2:
                way = self.castle(move_d, piece)
                if piece.color == self.bot_color:
                    if way == "short":
                        self.king_pos = [move_d[0], 6]
                    elif way == "long":
                        self.king_pos = [move_d[0], 2]
                    else:
                        empty = Empty('None', move_d[0:2])
                        self.position[move_d[0]][move_d[1]] = empty
                        self.position[move_d[2]][move_d[3]] = piece
            # Al paso
            elif (piece.name == 'Pawn') and ((move_d[1] - move_d[3]) != 0) and (self.position[move_d[2]][move_d[3]].name == 'Empty'):
                empty = Empty('None', move_d[0:2])
                self.position[move_d[0]][move_d[1]] = empty
                if piece.color == 'b':
                    empty = Empty('None', [move_d[2]+1, move_d[3]])
                    self.position[move_d[2]+1][move_d[3]] = empty
                else:
                    empty = Empty('None', [move_d[2]-1, move_d[3]])
                    self.position[move_d[2]-1][move_d[3]] = empty
                self.position[move_d[2]][move_d[3]] = piece
            else:
                empty = Empty('None', move_d[0:2])
                self.position[move_d[0]][move_d[1]] = empty
                self.position[move_d[2]][move_d[3]] = piece
        self.print_board(move)

    def make_potential_move(self, move_d):
        piece = self.position[move_d[0]][move_d[1]]
        empty = Empty('None', move_d[0:2])
        potential_position = copy.deepcopy(self.position)
        potential_position[move_d[0]][move_d[1]] = empty
        potential_position[move_d[2]][move_d[3]] = piece
        return potential_position

    def get_position(self):
        return self.position

    def castle(self, move_d, piece):
        way = "short"
        king = piece
        self.position[move_d[0]][move_d[1]] = Empty('None', move_d[:2])
        if (move_d[3] > 4) and (self.short_castle_allowed == True):
            print("short castle")
            rook = self.position[move_d[2]][move_d[3]]
            rook_move = [move_d[2], move_d[3], move_d[0], 5]
            self.position[move_d[2]][move_d[3]] = Empty(
                'None', [move_d[2], move_d[3]])
            self.position[move_d[0]][5] = rook
            rook.move(rook_move)
            self.position[move_d[2]][6] = king
        elif (move_d[3] < 4) and (self.long_castle_allowed == True):
            way = "long"
            print("long castle")
            rook = self.position[move_d[2]][move_d[3]]
            rook_move = [move_d[2], move_d[3], move_d[0], 3]
            self.position[move_d[2]][move_d[3]] = Empty(
                'None', [move_d[2], move_d[3]])
            self.position[move_d[0]][3] = rook
            rook.move(rook_move)
            self.position[move_d[2]][2] = king
        else:
            way ="None"
        return way

    def is_legal_move(self, move_d):
        legal = False
        piece = self.position[move_d[0]][move_d[1]]
        togo = self.position[move_d[2]][move_d[3]]
        if piece.name == 'Empty':
            #print("There was no piece..")
            pass
        elif piece.color != self.bot_color:
            #print("Opponents piece..")
            pass
        # and abs(move_d[1] - move_d[3]) == 2:
        elif (piece.name == 'King') and (togo.name == 'Rook') and (togo.color == self.bot_color):
            print("CASTLE")
            short_allowed, long_allowed = piece.is_castle_allowed(self.position)
            self.short_castle_allowed = short_allowed
            self.long_castle_allowed = long_allowed
            if (move_d[3] > 5) and (short_allowed == True):
                legal = True
            if (move_d[3] < 5) and (long_allowed == True):
                legal = True
        else:
            if piece.name != 'Pawn':
                allowed_moves = piece.get_allowed_moves(self.position)
            else:
                allowed_moves = piece.get_allowed_moves(self.position, self.opponent_move)
            piece.clear_allowed_moves()
            print("Piece considered: ", piece.name, allowed_moves)
            paso = False
            for i in range(len(allowed_moves)):
                if (allowed_moves[i][0] == move_d[2]) and ((allowed_moves[i][1] == move_d[3])):
                    pot_pos = self.make_potential_move(move_d)
                    if piece.name != 'King':
                        king = pot_pos[self.king_pos[0]][self.king_pos[1]]
                        tmp_king_pos = king.box
                    else:
                        king = piece
                        tmp_king_pos = move_d[2:]
                    #print("NAME: ",king.name, self.king_pos)
                    if king.in_check(pot_pos, tmp_king_pos) == False:
                        #print("Origin", pot_pos[move_d[0]][move_d[1]].name)
                        # print("Destin",move_d[2],move_d[3])
                        legal = True
                        break
                    else:
                        self.print_potential_board(pot_pos)
                        self.debug_msg("******************")
                        self.debug_msg("CHECK!")
                        self.debug_msg("******************")
        if legal == False:
            #print("not legal")
            pass
        return legal
