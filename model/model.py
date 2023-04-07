from model.game import Game

class Model():
    def __init__(self):
        self.game_1 = Game()
        self.game_1.start()
        self.game_2 = Game()
        self.game_2.start()

        self.active_game = self.game_1
        self.active_name = "upper"
        self.inactive_game = self.game_2
        self.inactive_name = "lower"