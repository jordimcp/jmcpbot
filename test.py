#"/home/joma/pers/jmcpbot/databases/lichess_jmcpgeh_2021-01-06.pgn"
import chess.pgn

class Test():
  def __init__(self, database):            
    self.pgn = open(database)    
    self.game = chess.pgn.read_game(self.pgn)
  
  def create_move_files(self):    
    i = 0
    self.black_f = open("debug/black_moves.txt","w")
    self.white_f = open("debug/white_moves.txt","w")
    for move in self.game.mainline_moves():      
      if i %2 == 0:
        self.white_f.write(move.uci() + '\n')       
      else:
        self.black_f.write(move.uci() + '\n')
      i +=1
    self.white_f.close()
    self.black_f.close()

  def next_game(self):
    self.game = chess.pgn.read_game(self.pgn)
