import pygame
from pygame.locals import *
import sys
import random
from board import *
Aqua = (0, 255, 255)
Black = (0,   0,   0)
Blue = (0,  0, 255)
Silver = (192, 192, 192)
Fuchsia = (255,   0, 255)
Gray = (128, 128, 128)
Green = (0, 128,   0)
Lime = (0, 255,   0)
Purple = (128,  0, 128)
Red = (255,   0,   0)
White = (255, 255, 255)
Yellow = (255, 255,   0)


class Tablero():
    def make(self, w, h):
        pygame.init()
        pygame.font.init()
        self.board = Board('b')
        title = "Chessboard"
        pygame.display.set_caption(title)
        self.dis_w = w
        self.dis_h = h
        self.strokeH = self.dis_h/8
        self.strokeW = self.dis_w/8
        self.display = pygame.display.set_mode((self.dis_w, self.dis_h))
        self.display.fill(White)
        self.playGridY = []
        self.playGridX = []
        self.makeGrid()
        self.clicking = False
        self.grabbed_piece = None
        self.legal_moves = None
        self.last_move = [0, 0, 0, 0]

    def finish(self):
        pygame.quit
        sys.exit()

    def makeGrid(self):
        self.display.fill(Purple)
        for i in range(8):
            self.makeRows(i)

    def getPosGui(self, row, col, position):
        piece = position[7-row][col]
        return piece

    def makeRows(self, num):
        jump = 0
        c = 0
        position = self.board.get_position()
        if num % 2 != 0:
            c += 1
            jump = self.strokeW * c
        for row in range(4):
            pygame.draw.rect(self.display, White, [
                             jump, row+(num*self.strokeH), self.strokeW, self.strokeH])
            c += 2
            jump = self.strokeW * c

        myfont = pygame.font.SysFont('Comic Sans MS', 60)
        square = 0
        for col in range(8):
            piece = self.getPosGui(num, col, position)
            if piece.name != 'Empty':
                textsurface = myfont.render(
                    piece.color + piece.name[0], 1, Gray)
                self.display.blit(textsurface, (square, num*self.strokeH))
            square = self.strokeW*(col+1)
        pygame.display.update()

    def legalMoves(self, moves):
        position = self.board.get_position()
        print("legalmoves", moves)
        for num in range(8):
            jump = 0
            c = 0
            if num % 2 != 0:
                c += 1
                jump = self.strokeW * c
            for row in range(4):
                pygame.draw.rect(self.display, White, [
                                 jump, row+(num*self.strokeH), self.strokeW, self.strokeH])
                c += 2
                jump = self.strokeW * c

        for move in moves:
            for col in range(8):
                for row in range(8):
                    if row == (7-move[0]) and col == move[1]:
                        jump = self.strokeW * col
                        pygame.draw.rect(self.display, Green, [
                                         jump, (row*self.strokeH), self.strokeW, self.strokeH])

        myfont = pygame.font.SysFont('Comic Sans MS', 60)
        for num in range(8):
            square = 0
            for col in range(8):
                # position[num][col]
                piece = self.getPosGui(num, col, position)
                if piece.name != 'Empty':
                    textsurface = myfont.render(
                        piece.color + piece.name[0], 1, Gray)
                    self.display.blit(textsurface, (square, num*self.strokeH))
                square = self.strokeW*(col+1)
        pygame.display.update()

    def find_idx(self, x, y):
        row = 0
        col = 0
        for r in range(8):
            for c in range(8):
                if y > (r*self.strokeW):
                    row = r
                if x > (c*self.strokeH):
                    col = c
        return row, col

    def get_piece(self, row, col):
        position = self.board.get_position()
        piece = self.getPosGui(row, col, position)  # position[row][col]
        if piece.name != 'Pawn':
            moves = piece.get_allowed_moves(position)
        else:
            moves = piece.get_allowed_moves(position, self.last_move)
        piece.clear_allowed_moves()
        self.legalMoves(moves)
        return piece, moves

    def drop_piece(self, row, col, piece):
        pos = piece.box
        d_col = {0: 'a', 1: 'b', 2: 'c', 3: 'd',
                 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        move_o = d_col[pos[1]] + str(pos[0]+1)
        move_d = d_col[col] + str(row+1)
        # move_d = d_col[col] + str(row)
        move = move_o + move_d
        if piece.name == "King":
            if ((col - pos[1]) == 2):
                if piece.color == 'w':
                    move = 'e1h1' #lichess annotation for castle
                else:
                    move = 'e8h8' #lichess annotation for castle
            if ((col - pos[1]) == -2):
                if piece.color == 'w':
                    move = 'e1a1' #lichess annotation for castle
                else:
                    move = 'e8a8' #lichess annotation for castle
        print(move)
        self.board.update_board(move)
        self.makeGrid()
        return move

    def whereClicked(self, x, y):
        row, col = self.find_idx(x, y)
        self.clicking = not self.clicking
        if self.clicking:
            self.grabbed_piece, self.legal_moves = self.get_piece(row, col)
            print(self.grabbed_piece.name + self.grabbed_piece.color)
        else:
            if self.grabbed_piece.color == 'w':
                move = [7-row, col]
                print(move)
                if move in self.legal_moves:
                    self.last_move = [self.grabbed_piece.box[0],
                                      self.grabbed_piece.box[1], move[0], move[1]]
                    move_str = self.drop_piece(7-row, col, self.grabbed_piece)
                    self.board.set_opponent_move(move_str)
                else:
                    print("Illegal")
            else:
                move = [self.grabbed_piece.box[0],
                        self.grabbed_piece.box[1], 7-row, col]
                print("Black move: ", move)
                if self.board.is_legal_move(move):
                    self.last_move = [self.grabbed_piece.box[0],
                                      self.grabbed_piece.box[1], move[0], move[1]]
                    move_str = self.drop_piece(7-row, col, self.grabbed_piece)
                else:
                    print("Illegal")


if __name__ == "__main__":
    tablero = Tablero()
    tablero.make(640, 640)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                tablero.finish()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                tablero.whereClicked(x, y)
