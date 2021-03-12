class Piece:
  def __init__(self,color,box):    
    self.color = color
    self.box = box
    self.boxes_to_move = []    
  
  def clear_allowed_moves(self):
    self.boxes_to_move = []
  
  def is_defended(self,position):
    if self.color == 'w':
        direction = 1
    else:
      direction = -1
    piece_row = self.box[0]
    piece_col = self.box[1]        
    print("IS DEFENDED:", piece_row, piece_col)
    defended = False
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
      if defended == False:
        while(keep):                
          if (piece_row + r > 7) or (piece_row + r < 0) or (piece_col + c > 7) or (piece_col + c < 0):
            keep = False                  
          else:          
            pot_piece = position[piece_row + r][piece_col + c]      
            if(j < 4): #Diagonals
              if ((r == 1) or (r == -1)) and ((c == 1) or (c == -1)):
                if pot_piece.name == 'Empty':
                  pass
                elif pot_piece.color != self.color:
                  keep = False
                elif pot_piece.color == self.color and (pot_piece.name == 'Queen' or pot_piece.name == 'Bishop' \
                    or (pot_piece.name == 'Pawn' and  step_r*direction < 0)or (pot_piece.name == 'King')):
                  defended = True                   
                  print("hola", j)
                  keep = False
                else:
                  keep = False
              else:
                if pot_piece.name == 'Empty':
                  pass
                elif pot_piece.color != self.color:
                  keep = False
                elif (pot_piece.color == self.color) and ((pot_piece.name == 'Queen') or (pot_piece.name == 'Bishop')):
                  defended = True                     
                  keep = False
                else:
                  keep = False

            elif(j >= 4): #vertical and horizontal
              if ((r == 1) or (r == -1)) or ((c == 1) or (c == -1)):
                if pot_piece.name == 'Empty':
                  pass
                elif pot_piece.color != self.color:
                  keep = False
                elif (pot_piece.color == self.color) and ((pot_piece.name == 'Queen') or (pot_piece.name == 'Rook') or (pot_piece.name == 'King')):
                  defended = True
                  keep = False
                else:
                  keep = False
              else:
                if pot_piece.name == 'Empty':
                  pass
                elif (pot_piece.color != self.color):
                  keep = False                
                elif pot_piece.color == self.color and ((pot_piece.name == 'Queen') or (pot_piece.name == 'Rook')):
                  defended = True                  
                  keep = False
                else:
                  keep = False
          r += step_r
          c += step_c  
    #checking knight
    knight_pos = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
    for pos in knight_pos:
      check_row  = (piece_row + pos[0])
      check_col = (piece_col + pos[1])
      if (check_row < 0) or (check_row > 7) or (check_col < 0) or (check_col > 7):
        pass
      else:
        if (position[check_row][check_col].name == 'Knight') and (position[check_row][check_col].color == self.color):
          defended = True              
          break
    return defended