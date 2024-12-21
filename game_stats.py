
class Game_stats:
    def __init__(self,ai_game):
        self.setting = ai_game.setting
        self.aliens_deleted = 0
        self.reset_stat()


    def reset_stat(self):
        self.aliens_deleted = 0
        self.ships_left = self.setting.ship_limit
       
