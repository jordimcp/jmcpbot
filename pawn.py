from piece import *

class Pawn(Piece):
  def __init__(self,color,box):
    super().__init__(color,box) 
    self.name = 'Pawn'
    self.ever_moved = False

  def move(self,move):    
    self.ever_moved = True
    self.box = move[2:]
  
  def get_allowed_moves(self,position,opponent_move):
    #Pawn can move vertical (2 boxes at the beginning), capture in diagonal 1 box, and al paso    
    current_row = self.box[0]
    current_col = self.box[1]  

    allow_al_paso = False
    opp_piece = position[opponent_move[2]][opponent_move[3]]
    print("Opp piece:", opp_piece.name, opponent_move, current_row)
    if (opp_piece.name == 'Pawn' ) and (abs(opponent_move[0] - opponent_move[2]) == 2) and (abs(opp_piece.box[1] - current_col) == 1) and (opponent_move[2] == current_row): 
      allow_al_paso = True      
       
    ways_to_check = 3 
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
          if (pot_piece.color != self.color) and (pot_piece.name != 'Empty') :            
            self.boxes_to_move.append([current_row + r, current_col+c])                      
    
    if allow_al_paso == True:
      print("Allow al passo")
      r = 1 * direction
      if (opp_piece.box[1] - current_col) == 1: #can take to the right
        self.boxes_to_move.append([current_row + r, current_col+1])        
      else:#can take to the left
        self.boxes_to_move.append([current_row + r, current_col-1])    

    return self.boxes_to_move
