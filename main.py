# docs https://berserk.readthedocs.io/en/master/
import berserk
from game import *
from time import sleep
from datetime import datetime
import chess.pgn
import chess
import io
import pickle 

def getMyGames(user,filename):
    print('Exporting games of: ', user)
    start = berserk.utils.to_millis(datetime(2018, 6, 15))
    end = berserk.utils.to_millis(datetime(2021, 1, 30))
    games_ex = client.games.export_by_player(user, as_pgn=True,since=start, until=end)
    d_l = []
    games = list(games_ex)
    n_game = 0
    for game in games:
        pgn = io.StringIO(game)
        curr_game = chess.pgn.read_game(pgn)
        board = chess.Board()
        result = curr_game.headers["Result"]
        white = curr_game.headers["White"]
        black = curr_game.headers["Black"]
        save = False
        if (result == '1-0') and (white == 'jmcpgeh'):
            save = True
        if (result == '0-1') and (black == 'jmcpgeh'):
            save = True
        if save:
            fenlist = []
            fenlist.append(board.fen())
            for m in curr_game.mainline_moves():
                move = chess.Move.from_uci(str(m))
                board.push(move)
                fenlist.append(board.fen()) 
            d = {result:fenlist}
            d_l.append(d)
            n_game += 1
            print("Games downloaded: ",n_game);
    print("Finished exporting")
    dump_file = open(filename,"wb")
    pickle.dump(d_l,dump_file)
    dump_file.close()

def testMyGames(filename):
    a_file = open(filename,"rb")
    output = pickle.load(a_file)
    for o in output:
        print(o.keys())
    a_file.close()

f = open("../../tokens/token.txt","r")
session = berserk.TokenSession(f.read())
client = berserk.Client(session)
info = client.account.get()
filename = "jmpcgeh_winning_fen.pkl"
print("On air: ", info["seenAt"])
#getMyGames('jmcpgeh',filename)
#testMyGames(filename)

for event in client.bots.stream_incoming_events():
  if event['type'] == 'challenge':    
    print("challeng ack")
    challenge_id = event['challenge']['id']    
    client.bots.accept_challenge(challenge_id)        
  elif event['type'] == 'gameStart':    
    game_id =event['game']['id']    
    game = Game(client, game_id)
    game.run()
