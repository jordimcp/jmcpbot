from piece import *

class Empty(Piece):
    def __init__(self,color,box):
      super().__init__(color,box) 
      self.name = 'Empty'