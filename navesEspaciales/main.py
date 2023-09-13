import pygame, random


SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

pygame.display.set_caption('Juego de Naves Espaciales')

BLACK =(0,0,0)
WHITE =(255,255,255)



class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
    def update(self):
        self.rect.y += 1
        
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -10
            self.rect.x= random.randrange(SCREEN_WIDTH)
            
        

class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x=mouse_pos[0]
        self.rect.y=mouse_pos[1]
        

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image =pygame.image.load("laser.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
    def update (self):
        self.rect.y-=5


    
class Game(object):
    
    def __init__(self):
        
        self.game_over = False
        self.score=0
        self.sound = pygame.mixer.Sound("laser5.ogg")
        
        self.meteor_list = pygame.sprite.Group()
        self.meteor_hit_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        
        for i in range(50):
            meteor1 = Meteor()
            meteor1.rect.x = random.randrange(900)
            meteor1.rect.y= random.randrange(600)
            
            self.meteor_list.add(meteor1)
            self.all_sprites_list.add(meteor1)


        self.player = Player()

        self.all_sprites_list.add(self.player)

    
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over:
                    laser=Laser()
                    laser.rect.x=self.player.rect.x +45
                    laser.rect.y = self.player.rect.y -20
                    
                    self.all_sprites_list.add(laser)
                    self.laser_list.add(laser)
                    self.sound.play()
                
                if self.game_over:
                    self.__init__()
        return False
        
    def run_logic(self):
        
        if not self.game_over:
            self.all_sprites_list.update()
            
            for laser in self.laser_list:
                meteor_hit_list = pygame.sprite.spritecollide(laser, self.meteor_list, True)
                for meteor in meteor_hit_list:
                    self.all_sprites_list.remove(laser)
                    self.laser_list.remove(laser)
                    self.score+=1
                    print(self.score)
                if laser.rect.y < -10:
                    self.all_sprites_list.remove(laser)
                    self.laser_list.remove(laser)
                
            
            if len(self.meteor_list) == 0:
                self.game_over = True
    
    
    def display_frame(self,screen,background):
        screen.blit(background,[0,0])
        
        if self.game_over:
            font = pygame.font.SysFont("serif", 35)
            text = font.render("Game Over, Click To Continue", True, WHITE)
            center_x= (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y= (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
        
        
        
        if not self.game_over:
            self.all_sprites_list.draw(screen)
        
        pygame.display.flip()

def main():
    pygame.init()
    
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    
    background = pygame.image.load("background.png").convert()

    done=False
    
    clock = pygame.time.Clock()
    
    game = Game()
    
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen, background)
        clock.tick(60)
    pygame.quit()



if __name__=="__main__":
    main()