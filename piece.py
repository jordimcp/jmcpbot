class Piece:
  def __init__(self,color,box):    
    self.color = color
    self.box = box
    self.boxes_to_move = []    
  
  def clear_allowed_moves(self):
    self.boxes_to_move = []