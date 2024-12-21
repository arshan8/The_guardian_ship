
class Settings:
    def __init__(self):
        self.bgcolor = (36,36,62)
        self.screen_width = 1200
        self.screen_hight = 600
        self.ship_speed = 11

        self.bullet_speed = 7
        self.bullet_width = 20
        self.bullet_height = 25
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 2

        self.alien_speed = 7
        self.fleet_drop_speed = 15
 # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = -1

        self.ship_limit = 2

#     def display(self):
#         print(f" current setting status: width = {self.screen_width}")

# s1 = Settings()
# s1.display()