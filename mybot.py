import berserk
import threading
import chess.pgn
from board import *
from test import *

class Bot():
  def __init__(self, bot_id, color):    
    self.id = bot_id
    self.color = color   
    self.pgn = open("/home/joma/pers/jmcpbot/databases/lichess_jmcpgeh_2021-01-06.pgn")
    self.board = Board(self.color[0])
    self.turn = 0 # debug

  def get_color(self):
    return self.color  

  def get_id(self):
    return self.id

  def start_game(self):
    self.board.init_board()
    self.turn = 0

  def silly_alg(self,opponent_move):
    first_game = chess.pgn.read_game(self.pgn)    
    for move in first_game.mainline_moves():
      print(move)

  def move_whatever_legal(self,opponent_move):    
    col = ['a','b','c','d','e','f','g','h']
    row = [1,2,3,4,5,6,7,8]
    #f = open("debug/black_moves.txt","r")
    #result = f.read()
    #moves = result.split("\n")
    #bot_move = "move"
    #if self.turn >= len(moves)-1:
    #  print("Game FINISHED no more moves")
    #else:
      #bot_move = moves[self.turn]    
      #print("Black moves", bot_move)
      #self.turn += 1
    legal = False
    #legal = self.board.is_legal(bot_move)    
    for c in range(8):
      for r in range(8):
        c_o = col[c]
        r_o = str(row[r])
        for i in range(8):
          for k in range(8):
            c_f= col[i]
            r_f = str(row[k])
            bot_move = c_o+r_o+c_f+r_f                       
            legal = self.board.is_legal(bot_move)
            if legal:
              break;
          if legal:
            break;
        if legal:
          break;
      if legal:
        break;
    if legal:
      print(bot_move)
      self.board.update_board(bot_move)    
      #f.close()
    else:
      print("Move not legal")
      self.board.debug_msg("********************")
      self.board.debug_msg(("ERROR:TURN NOT LEGAL (move was: %s)") %(bot_move))
      self.board.debug_msg("********************")
      #assert( 1 == 0)
    return bot_move  
    
  def make_decision(self,opponent_move):  
    self.board.set_opponent_move(opponent_move)  
    self.board.update_board(opponent_move)
    bot_move = self.move_whatever_legal(opponent_move)
    return bot_move


## Debug

# def setup_next_game(bot):
#   bot.start_game()
#   f=open("debug/white_moves.txt","r")
#   result = f.read()
#   moves = result.split("\n")[:-1]
#   f.close()
#   return moves
# while True:
#   bot = Bot('BOT','black')  
#   test = Test("/home/joma/pers/jmcpbot/databases/lichess_jmcpgeh_2021-01-06.pgn")
#   test.create_move_files()
#   total_games = 1000
#   for i in range(total_games):
#     moves = setup_next_game(bot)
#     for m in moves:   
#       print("White moves:", m) 
#       bot.make_decision(m)         
#     test.next_game()
#     if i < total_games-1:
#       test.create_move_files()
#   break