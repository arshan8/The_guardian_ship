import pygame
import sys
from Sts_f import Settings
from ship import Ship
from bullet import Bullet
from alein import Alien
from time import sleep
from game_stats import Game_stats
from button import Button



class The_guardian_ship:
    def __init__(self):
        
        pygame.init()
        pygame.mixer.init()
        self.setting = Settings()
        #self.ship = Ship(self)
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_hight)) #object = surface
       # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) #object = surface
        pygame.display.set_caption('The_guardian_ship')
        self.bgcolor = self.setting.bgcolor
        self.clock = pygame.time.Clock()

        self.ship = Ship(self)
        self.stats = Game_stats(self)


        self.bullets =pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        

        
        self.font = pygame.font.SysFont(None, 25)
        self.game_active = False

        self.play_button = Button(self, "play Again")

        pygame.mixer.music.load('sound/backgroundmusic.mp3')
        pygame.mixer.music.play(-1)
        
        pygame.mixer.music.load('sound/backgroundmusic.mp3')
        pygame.mixer.music.play(-1)
        # pygame.mixer.music.play(-1)

        self.ship_hit_sound = pygame.mixer.Sound('sound/whencollide.mp3')
        self.game_over_sound = pygame.mixer.Sound('sound/gameover.mp3')



    def run_game(self):
        while True :
            self._check_events()
            self._update_screen()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                #self.bullets.update()
                self._update_aliens()
               
            # self.ship.blitme()  
            # pygame.display.flip()
           # self.clock.tick(60)
        #     # self.screen.fill(self.bgcolor)   
        #     for bullet in self.bullets.copy():   #delete bullets once they reach top head
        #          if bullet.rect.bottom <= 0:
        #         # if bullet.rect.y <= 0:
        #               self.bullets.remove(bullet)
        #   #  print(len(self.bullets))

    def _check_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:  # Check if the close button was clicked
                pygame.quit()  # Properly quit Pygame
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_pos = pygame.mouse.get_pos()
                 if self.play_button.rect.collidepoint(mouse_pos):
                     # self.stats.aliens_deleted
                      self.game_active = True
                      
                      self.aliens.empty()
                      self.stats.reset_stat()
                      pygame.mixer.music.play(-1)
                      

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            # elif event.key == pygame.K_q:
            #     sys.exit()
                     
    def _update_screen(self):
 
         self.ship.blitme()  
         self.aliens.draw(self.screen)

         if not self.game_active:
              self.play_button.draw_button()
         pygame.display.flip()
         self.clock.tick(60)
         self.screen.fill(self.bgcolor)
         for bullet in self.bullets.sprites():
              bullet.draw_bullet()
         self._show_aliens_deleted()


    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()
        elif event.key == pygame.K_q:
                sys.exit()

    def _check_keyup_events(self,event):
        #do not write this for left moment if u want automatically left and just keep draggingf right 
                #but self.rect.x for right must be much high than self.rect.left
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
         if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
         
         self.bullets.update()
         for bullet in self.bullets.copy():   #delete bullets once they reach top head
                 if bullet.rect.bottom <= 0:
                # if bullet.rect.y <= 0:
                      self.bullets.remove(bullet)
         collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
         
         if not self.aliens:
              self.bullets.empty()
              self._create_fleet()
        
                 
         
    def _create_fleet(self):
         
         alienne = Alien(self)
         alienne_width,alienne_height = alienne.rect.size
         #self.aliens.add(alienne)
         

         current_x,current_y = alienne_width, alienne_height
         while current_y < (self.setting.screen_hight - 5 * alienne_height):
            while current_x <  (self.setting.screen_width - 2 * alienne_width):
                self._create_alien(current_x,current_y)
                current_x += 2* alienne_width
            current_x = alienne_width
            current_y += 2* alienne_height

    def _create_alien(self,current_x,current_y):
        new_alien = Alien(self)
        new_alien_x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)

    def _update_aliens(self):
         self._check_fleet_edges()
         self.aliens.update()
         for alien in self.aliens.copy():  # Copy to avoid modifying the group while iterating
            if alien.rect.bottom >= self.setting.screen_hight:
                self.aliens.remove(alien)
                self.stats.aliens_deleted += 1
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._ship_hit()
              
              
            
         
    def _check_fleet_edges(self):
            """Respond appropriately if any aliens have reached an edge."""
            for alien in self.aliens.sprites():
                if alien.check_edges():
                    self._change_fleet_direction()
                    break
                 
    def _change_fleet_direction(self):
         for alien in self.aliens.sprites():
              alien.rect.y += self.setting.fleet_drop_speed
         self.setting.fleet_direction *= -1

    def _show_aliens_deleted(self):
        self.aliens_deleted = self.stats.aliens_deleted
        #self.aliens_deleted = Game_stats.alie
    
        counter_str = f"INVADED: {self.aliens_deleted}"
        counter_image = self.font.render(counter_str, True, (200, 2, 10), self.bgcolor)

        counte_str = f"SHIP LEFT: {self.stats.ships_left + 1 }"
        counte_image = self.font.render(counte_str, True, (200,2, 10), self.bgcolor)

        # Create a rectangle to position the text in the top-left corner
        counter_rect = counter_image.get_rect()
        counter_rect.topleft = (10, 10)  # Positioning at the top-left corner

        counte_rect = counter_image.get_rect()
        counte_rect.topright = (1000,10)  # Positioning at the top-left corner

        # Draw the text on the screen
        self.screen.blit(counter_image, counter_rect)
        self.screen.blit(counte_image, counte_rect)



    def _ship_hit(self):
        
        if self.stats.ships_left > 0:
            pygame.mixer.music.pause()
            self.ship_hit_sound.play()


            self.stats.ships_left -=1
            self.stats.aliens_deleted += len(self.aliens)

           # self.ship.rect = (0,200,0)

            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet
            
        
            sleep(2)
            self.ship.rect.midbottom = (self.setting.screen_width//2,self.setting.screen_hight)
            pygame.mixer.music.unpause()

        else:
             self.game_active = False
             pygame.mixer.music.stop()
             self.game_over_sound.play()
             


         
if __name__ == '__main__':
    ai = The_guardian_ship()
    ai.run_game()

 
 #next plan:  add no. of aliens destroyed text in middle , and add sound effects too for ship collision etc