from piece import *

class King(Piece):
  def __init__(self,color,box):
    super().__init__(color,box) 
    self.name = 'King'
    self.can_castle = True

  def move(self,move):
    self.can_castle = False
    self.box = move[2:]
  
  def get_allowed_moves(self,position):
    #King can move diagonal and vertical and horizontal but one box only
    current_row = self.box[0]
    current_col = self.box[1]    
    for j in range(8): # always has 8 ways to check
      keep = True
      if j == 0:
          step_r = 1
          step_c = 1
          r = 1
          c = 1
      elif j == 1:
          step_r = 1
          step_c = -1
          r = 1
          c = -1
      elif j == 2:
          step_r = -1
          step_c = 1
          r = -1
          c = 1
      elif j == 3:
          step_r = -1
          step_c = -1
          r = -1
          c = -1    
      elif j == 4:
          step_r = 1
          step_c = 0
          r = 1
          c = 0
      elif j == 5:
          step_r = -1
          step_c = 0
          r = -1
          c = 0
      elif j == 6:
          step_r = 0
          step_c = 1
          r = 0
          c = 1
      elif j == 7:
          step_r = 0
          step_c = -1
          r = 0
          c = -1        
      if (current_row + r > 7) or (current_row + r < 0) or (current_col + c > 7) or (current_row + c < 0):
        keep = False                  
      else:          
        pot_piece = position[current_row + r][current_col + c]      
        if pot_piece.name == 'Empty':
          self.boxes_to_move.append([current_row + r, current_col+c])        
        elif (pot_piece.color != self.color) and (pot_piece.name != 'Empty') :
          self.boxes_to_move.append([current_row + r, current_col+c])        
          keep = False
        else:
          keep = False      
    return self.boxes_to_move

  def in_check(self,position,king_pos):
    #check if the first thing in diagonals from king are bishops or queens or pawns of the other color
    #check if the first thing in vertical from king are rooks or queens
    #check if knight
    if self.color == 'w':
      direction = 1
    else:
      direction = -1
      
    in_check = False
    king_row = king_pos[0]
    king_col = king_pos[1]        
    print(position[king_pos[0]][king_pos[1]].name)
    print(king_row,king_col)
    for j in range(8): # always has 8 ways to check
      keep = True
      if j == 0:
          step_r = 1
          step_c = 1
          r = 1
          c = 1
      elif j == 1:
          step_r = 1
          step_c = -1
          r = 1
          c = -1
      elif j == 2:
          step_r = -1
          step_c = 1
          r = -1
          c = 1
      elif j == 3:
          step_r = -1
          step_c = -1
          r = -1
          c = -1    
      elif j == 4:
          step_r = 1
          step_c = 0
          r = 1
          c = 0
      elif j == 5:
          step_r = -1
          step_c = 0
          r = -1
          c = 0
      elif j == 6:
          step_r = 0
          step_c = 1
          r = 0
          c = 1
      elif j == 7:
          step_r = 0
          step_c = -1
          r = 0
          c = -1       
      if in_check == False:
        while(keep):                
          if (king_row + r > 7) or (king_row + r < 0) or (king_col + c > 7) or (king_col + c < 0):
            keep = False                  
          else:          
            pot_piece = position[king_row + r][king_col + c]      
            if(j < 4): #Diagonals
              if ((r == 1) or (r == -1)) and ((c == 1) or (c == -1)):
                if pot_piece.name == 'Empty':
                  pass
                elif pot_piece.color == self.color:
                  keep = False
                elif pot_piece.color != self.color and (pot_piece.name == 'Queen' or pot_piece.name == 'Bishop' \
                    or (pot_piece.name == 'Pawn' and  step_r*direction > 0)or (pot_piece.name == 'King')):
                  in_check = True 
                  f = open ("debug/text.txt", "w")
                  f.write("Check\n")                  
                  f.write(pot_piece.name+ ' ' + str(pot_piece.box[0]) + str(pot_piece.box[1]))
                  f.close()
                  keep = False
              else:
                if pot_piece.name == 'Empty':
                  pass
                elif pot_piece.color == self.color:
                  keep = False
                elif (pot_piece.color != self.color) and ((pot_piece.name == 'Queen') or (pot_piece.name == 'Bishop')):
                  in_check = True                       
                  keep = False
            elif(j >= 4): #vertical and horizontal
              if ((r == 1) or (r == -1)) or ((c == 1) or (c == -1)):
                if pot_piece.name == 'Empty':
                  pass
                elif pot_piece.color == self.color:
                  keep = False
                elif (pot_piece.color != self.color) and ((pot_piece.name == 'Queen') or (pot_piece.name == 'Rook') or (pot_piece.name == 'King')):
                  in_check = True
                  keep = False
              else:
                if pot_piece.name == 'Empty':
                  pass
                elif (pot_piece.color == self.color):
                  keep = False                
                elif pot_piece.color != self.color and ((pot_piece.name == 'Queen') or (pot_piece.name == 'Rook')):
                  in_check = True                  
                  keep = False
          r += step_r
          c += step_c  
      if in_check == False:
        #checking knight
        knight_pos = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
        for pos in knight_pos:
          check_row  = (king_row + pos[0])
          check_col = (king_col + pos[1])
          if (check_row < 0) or (check_row > 7) or (check_col < 0) or (check_col > 7):
            pass
          else:
            if (position[check_row][check_col].name == 'Knight') and (position[check_row][check_col].color != self.color):
              in_check = True              
              break
    return in_check