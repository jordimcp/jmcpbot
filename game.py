import berserk
from mybot import *
import threading


class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.game_info = self.client.games.get_ongoing()[0]
        self.mybot = Bot("jmcpbot", self.game_info['color'])
        self.stream = self.client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
    
    def run(self):
        # if self.game_info['isMyTurn']:
        #    self.move()
        for event in self.stream:
            ko = 0
            finish = False
            print(event)
            if event['type'] == 'gameState':
                #print(type(event['moves']))
                move_list = event['moves'].split(' ')
                finish = self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                ko = self.handle_chat_line(event)
            if not finish:
                self.game_info = self.client.games.get_ongoing()[0]
                #print("Game Info: ", self.game_info)
                if self.game_info['isMyTurn']:
                    opp_move = move_list[-1]
                    #self.move(self.game_info['lastMove'])
                    self.move(opp_move)
                if ko == 1:
                    self.client.bots.resign_game(self.game_id)
                    break

    def move(self, opponent_move):
        print("Opponent move: ", opponent_move)
        bot_move = self.mybot.make_decision(opponent_move)
        print("Jmcpbot move: ", bot_move)
        self.client.bots.make_move(self.game_id, bot_move)

    def handle_state_change(self, event):
        gamefinished = False
        if event['status'] == 'mate':
            gamefinished = True
        return gamefinished

    def handle_chat_line(self, chat_line):
        ko = 0
        if(chat_line['username'] != "jmcpgeh"):
            if(chat_line['text'] != "abort"):
                self.client.bots.post_message(
                    self.game_id, 'Here we are! Lets do this!', spectator=False)
                self.client.bots.post_message(
                    self.game_id, 'Here we are! Lets do this!', spectator=True)
            else:
                ko = 1
        return ko
