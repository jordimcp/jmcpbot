from piece import *


class Knight(Piece):
    def __init__(self, color, box):
        super().__init__(color, box)
        self.name = 'Knight'

    def move(self, move):
        self.box = move[2:]

    def get_allowed_moves(self, position):
        # Knight can move 2 vertical and 1 horizontal, or 1 and 2
        current_row = self.box[0]
        current_col = self.box[1]
        for j in range(8):  # always has 8 boxes to check
            keep = True
            if j == 0:
                r = 2
                c = 1
            elif j == 1:
                r = 2
                c = -1
            elif j == 2:
                r = -2
                c = 1
            elif j == 3:
                r = -2
                c = -1
            elif j == 4:
                r = 1
                c = 2
            elif j == 5:
                r = -1
                c = 2
            elif j == 6:
                r = 1
                c = -2
            elif j == 7:
                r = -1
                c = -2

            if (current_row + r > 7) or (current_row + r < 0) or (current_col + c > 7) or (current_col + c < 0):
                keep = False
            else:
                pot_piece = position[current_row + r][current_col + c]
                if pot_piece.name == 'Empty':
                    self.boxes_to_move.append([current_row + r, current_col+c])
                elif (pot_piece.color != self.color) and (pot_piece.name != 'Empty'):
                    self.boxes_to_move.append([current_row + r, current_col+c])
                    keep = False
                else:
                    keep = False

        return self.boxes_to_move
