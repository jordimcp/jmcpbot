from piece import *


class Rook(Piece):
    def __init__(self, color, box):
        super().__init__(color, box)
        self.name = 'Rook'
        self.moved = False

    def move(self, move):
        self.box = move[2:]
        self.moved = True

    def get_allowed_moves(self, position):
        # Rook can move vertical and horizontal
        current_row = self.box[0]
        current_col = self.box[1]
        for j in range(4):  # always has 4 ways to check
            keep = True
            if j == 0:
                step_r = 1
                step_c = 0
                r = 1
                c = 0
            elif j == 1:
                step_r = -1
                step_c = 0
                r = -1
                c = 0
            elif j == 2:
                step_r = 0
                step_c = 1
                r = 0
                c = 1
            elif j == 3:
                step_r = 0
                step_c = -1
                r = 0
                c = -1
            while(keep):
                if (current_row + r > 7) or (current_row + r < 0) or (current_col + c > 7) or (current_col + c < 0):
                    keep = False
                else:
                    pot_piece = position[current_row + r][current_col + c]
                    if pot_piece.name == 'Empty':
                        self.boxes_to_move.append(
                            [current_row + r, current_col+c])
                    elif (pot_piece.color != self.color) and (pot_piece.name != 'Empty'):
                        self.boxes_to_move.append(
                            [current_row + r, current_col+c])
                        keep = False
                    else:
                        keep = False
                r += step_r
                c += step_c
        return self.boxes_to_move
