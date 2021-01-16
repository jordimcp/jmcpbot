# docs https://berserk.readthedocs.io/en/master/

import berserk
from game import *
from time import sleep
f = open("token.txt","r")
session = berserk.TokenSession(f.read())
client = berserk.Client(session)
info = client.account.get()
print("On air: ", info["seenAt"])


for event in client.bots.stream_incoming_events():
  if event['type'] == 'challenge':    
    print("challeng ack")
    challenge_id = event['challenge']['id']    
    client.bots.accept_challenge(challenge_id)        
  elif event['type'] == 'gameStart':    
    game_id =event['game']['id']    
    game = Game(client, game_id)
    game.run()
