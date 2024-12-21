import pygame

class Ship:
    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # self.image = pygame.image.load('images/blackship.bmp')

        self.image = pygame.image.load('images/blackship.bmp')

        # Get the original size of the image
        original_width, original_height = self.image.get_size()

        # Scale the image to 1/4th of its original size
        new_width = original_width // 7
        new_height = original_height // 7
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()

        
        self.rect.midbottom = self.screen_rect.midbottom

        self.rect.width = int(self.rect.width * 0.6)
        

        self.setting = ai_game.setting
        
    
        self.moving_right = False
        self.moving_left = False

    def update(self):                              #The update() method will be called from outside the class, so 
                                                                        #it’s not considered a helper method.
        if self.moving_right and self.rect.right < self.screen_rect.right:  #or s...<self.screen.get_rect.right 
            self.rect.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -=self.setting.ship_speed

    def blitme(self):
        self.screen.blit(self.image,self.rect)