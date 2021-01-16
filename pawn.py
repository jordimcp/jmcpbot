from piece import *

class Pawn(Piece):
  def __init__(self,color,box):
    super().__init__(color,box) 
    self.name = 'Pawn'
    self.ever_moved = False

  def move(self,move):    
    self.ever_moved = True
    self.box = move[2:]
  
  def get_allowed_moves(self,position):
    #Pawn can move vertical (2 boxes at the beginning), capture in diagonal 1 box, and al paso    
    current_row = self.box[0]
    current_col = self.box[1]     
    ways_to_check = 3 # TODO: Al paso
    if self.ever_moved == False:
      ways_to_check += 1
    direction = 1
    if self.color == 'b':
      direction = -1
    for j in range(ways_to_check): # always has 8 ways to check
      keep = True
      if j == 0:          
          r = 1 * direction
          c = 0
      elif j == 1:          
          r = 1 * direction
          c = 1
      elif j == 2:          
          r = 1 * direction
          c = -1
      elif j == 3:          
          r = 2 * direction
          c = 0            

      if (current_row + r > 7) or (current_row + r < 0) or (current_col + c > 7) or (current_col + c < 0):
        keep = False                  
      else:                               
        pot_piece = position[current_row + r][current_col + c]              
        if (j == 0) or (j == 3): #towards 1 or 2 boxes
          if pot_piece.name == 'Empty':
            self.boxes_to_move.append([current_row + r, current_col+c])        
        elif (j == 1) or (j == 2): # take diagonal          
          print("name pot:", pot_piece.name, "coord:", current_row + r ,current_col + c )
          if (pot_piece.color != self.color) and (pot_piece.name != 'Empty') :
            self.boxes_to_move.append([current_row + r, current_col+c])                          
    #TODO tomar al paso

    return self.boxes_to_move
