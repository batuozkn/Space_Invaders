from errno import ENOTEMPTY
import pygame, random, sys
from pygame.time import Clock


pygame.init()

size = width, height = 1200, 800
background = pygame.image.load("space 2.png")
back_rect = background.get_rect()
screen = pygame.display.set_mode(size)
Clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)


class Space_Invaders:
    def __init__(self):
        self._number_of_bullets = 20
        self._score = 0
        self._font = pygame.font.SysFont('aliases',35)
        self._font2 = pygame.font.SysFont('aliases',100)    
        self._gamepaused = False
        self._spaceship = None
        self._enemies = []
        self._allies = []
        

    def __del__(self):
        print("object deleted")

    def start(self):
        self._spaceship = Spaceship()
        for i in range(3):
            self._enemies.append(Enemy_1())
            self._enemies.append(Enemy_2())
            self._enemies.append(Enemy_3())
            self._allies.append(Ally())

    def display_score_numbullets(self):
        score_surf = self._font.render(f'SCORE: {self._score}',False,'green')
        score_rect = score_surf.get_rect(topleft=(20,20))
        screen.blit(score_surf,score_rect)
        score_surf2 = self._font.render(f'Remain Bullets: {self._number_of_bullets}',False,'red')
        score_rect2 = score_surf2.get_rect(topright=(1180,20))
        screen.blit(score_surf2,score_rect2)  

    def display_start_screen(self):
        text_surf = self._font2.render('press ENTER to start the game',False,'white')
        text_rect = text_surf.get_rect(topleft=(100,350))
        screen.blit(text_surf,text_rect)  

    def restart(self):
        self.exit_game()
        self.start()

    def pause_resume(self): # stopes and restarts the while loop
        if self._gamepaused == False:
            self._gamepaused = True
        elif self._gamepaused == True:
            self._gamepaused = False
        
    def exit_game(self): 
        self._spaceship = None
        for enemy in self._enemies:
            self._enemies.remove(enemy)
            enemy = None
        for ally in self._allies:
            self._allies.remove(ally)
            ally = None
        self.get_default()



    def shoot(self):
        self._spaceship.create_bullet()
       

    def move_ship(self, change):
        self._spaceship.move_spaceship(change)

    def hit_ally(self, ally): 
        self._number_of_bullets -= 2
        self._score -= 10
        self._allies.remove(ally)
        ally = None
        self._allies.append(Ally())
        
    def hit_enemy(self, enemy): 
        self._number_of_bullets += 1
        self._score += 10
        self._enemies.remove(enemy)
        enemy = None
        new_enemy = random.choice([Enemy_1(), Enemy_2(), Enemy_3()])
        self._enemies.append(new_enemy)


    def get_default(self):
        self._number_of_bullets = 20
        self._score = 0
        self._gamepaused = False

    def iscollision(self, bullet): 
        for enemy in self._enemies:
            if bullet != None:
                if pygame.Rect.colliderect(bullet.return_rect(), enemy.return_rect()):
                    self.hit_enemy(enemy)
                    self._spaceship.return_bullet_list().remove(bullet)
                    bullet = None
            
                
        for ally in self._allies:
            if bullet != None:
                if pygame.Rect.colliderect(bullet.return_rect(), ally.return_rect()):
                    self.hit_ally(ally)
                    self._spaceship.return_bullet_list().remove(bullet)
                    bullet = None

        if bullet != None and bullet.return_rect().bottom < 0:
            self._spaceship.return_bullet_list().remove(bullet)
            bullet = None

    def bullet_dec(self):
        self._number_of_bullets -= 1

    def bullet_num(self):
        return self._number_of_bullets
    
           


class SpaceObjects:
    def __init__(self):
        self._x = random.randint(64, 1200)
        self._y = random.randint(0, 200)
        self._waitingtime = random.randint(1,100)
        self._direction_x = random.randint(1, 3)
        self._direction_y = random.randint(1, 3)
        self._direction = [self._direction_x, self._direction_y]

    def __del__(self):
        print("object deleted")
    
    def move_spaceobjects(self): 
        self._timesincelastmove = self._timesincelastmove + Clock.get_time()
        if self._timesincelastmove >= self._waitingtime:
            self._timesincelastmove = 0
            self._rect = self._rect.move(self._direction)
            if self._rect.left < 0 or self._rect.right > width:
                self._direction[0] = -self._direction[0]
            if self._rect.top < 0 or self._rect.bottom > height - 300:
                self._direction[1] = -self._direction[1]


class Enemy_1(SpaceObjects):
    def __init__(self):
        self._image_enemy1 = pygame.image.load("1_64x64.png")
        self._rect = self._image_enemy1.get_rect()
        super().__init__()
        self._rect.right = self._x
        self._rect.top = self._y
        self._timesincelastmove = 0
        
    
    def return_image(self):
        return self._image_enemy1

    def return_rect(self):
        return self._rect

    def __del__(self):
        print("object deleted")


class Enemy_2(SpaceObjects):
    def __init__(self):
        self._image_enemy2 = pygame.image.load("3_64x64.png")
        self._rect = self._image_enemy2.get_rect()
        super().__init__()
        self._rect.right = self._x
        self._rect.top = self._y
        self._timesincelastmove = 0 
    
    def return_image(self):
        return self._image_enemy2

    def return_rect(self):
        return self._rect

    def __del__(self):
        print("object deleted")
        

class Enemy_3(SpaceObjects):
    def __init__(self):
        self._image_enemy3 = pygame.image.load("4_64x64.png")
        self._rect = self._image_enemy3.get_rect()
        super().__init__()
        self._rect.right = self._x
        self._rect.top = self._y
        self._timesincelastmove = 0

    def return_image(self):
        return self._image_enemy3

    def return_rect(self):
        return self._rect

    def __del__(self):
        print("object deleted")
        

class Bullet:
    def __init__(self):
        self._image_bullet = pygame.image.load("bullet_2.png")
        self._bullet = self._image_bullet.get_rect()
        self._bullet.right , self._bullet.top = self.location_of_bullet()
        self._direction = [0, -3]
        self._timesincelastmove = 0
        self._waitingtime = 7

    def __del__(self):
        print("object deleted")

    def move_bullet(self):
        self._timesincelastmove = self._timesincelastmove + Clock.get_time()
        if self._timesincelastmove >= self._waitingtime:
            self._timesincelastmove = 0
            self._bullet = self._bullet.move(self._direction)

    def location_of_bullet(self): 
        return SpaceInvaders._spaceship.location()


    def return_image(self):
        return self._image_bullet

    def return_rect(self):
        return self._bullet


class Ally(SpaceObjects):
    def __init__(self):
        self._image_earth = pygame.image.load("earth_64x64.png")
        self._rect = self._image_earth.get_rect()
        super().__init__()
        self._rect.right = self._x
        self._rect.top = self._y
        self._timesincelastmove = 0
        
    def __del__(self):
        print("object deleted")  
    
    def return_image(self):
        return self._image_earth

    def return_rect(self):
        return self._rect
    
    



class Spaceship:
    def __init__(self):
        self._image_spaceship = pygame.image.load("spaceship_64x64.png")
        self._spaceship_rect = self._image_spaceship.get_rect()
        self._spaceship_rect.right = random.randint(64, 1200)
        self._spaceship_rect.top = 700
        self._bullet = []

    def __del__(self):
        print("object deleted")

    def return_bullet_list(self):
        return self._bullet
    
    def return_image(self):
        return self._image_spaceship

    def return_rect(self):
        return self._spaceship_rect
        
    def create_bullet(self):
        if SpaceInvaders.bullet_num() > 0:
            self._bullet.append(Bullet())
            SpaceInvaders.bullet_dec()
        
 

    def move_spaceship(self,change): 
        if change < 0:
            if self._spaceship_rect.right > 74:
                self._spaceship_rect.right += change
        else:
            if self._spaceship_rect.right < 1190:
                self._spaceship_rect.right += change

    def location(self):
        return self._spaceship_rect.right -24 , self._spaceship_rect.top # -24 is to create bullet at the middle point of the spaceship (spaceship)




SpaceInvaders = Space_Invaders()


while True:
    Clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if SpaceInvaders._spaceship == None:
                    SpaceInvaders.start()

            elif event.key == pygame.K_e:
                SpaceInvaders.exit_game()

            elif event.key == pygame.K_SPACE:
                if SpaceInvaders._spaceship and SpaceInvaders._gamepaused == False:
                    SpaceInvaders._spaceship.create_bullet()

            elif event.key == pygame.K_p:
                if SpaceInvaders._spaceship:
                    SpaceInvaders.pause_resume()

            elif event.key == pygame.K_r:
                if SpaceInvaders._spaceship:
                    SpaceInvaders.restart()
            

    if SpaceInvaders._spaceship and SpaceInvaders._gamepaused == False:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            change = +2
            SpaceInvaders.move_ship(change)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            change = -2
            SpaceInvaders.move_ship(change)

               
    
    if SpaceInvaders._spaceship:
        screen.blit(background, back_rect)
        SpaceInvaders.display_score_numbullets()
        if SpaceInvaders._enemies != []:
            for enemy in SpaceInvaders._enemies:
                screen.blit(enemy.return_image(), enemy.return_rect())
                if SpaceInvaders._gamepaused == False:
                    enemy.move_spaceobjects()
        if SpaceInvaders._allies != []:
            for ally in SpaceInvaders._allies:
                screen.blit(ally.return_image(), ally.return_rect())
                if SpaceInvaders._gamepaused == False:    
                    ally.move_spaceobjects()
        screen.blit(SpaceInvaders._spaceship.return_image(), SpaceInvaders._spaceship.return_rect())
        if SpaceInvaders._spaceship._bullet != []:
            for bullet in SpaceInvaders._spaceship._bullet:
                screen.blit(bullet.return_image(), bullet.return_rect())
                if SpaceInvaders._gamepaused == False:
                    bullet.move_bullet()
                    SpaceInvaders.iscollision(bullet)
        pygame.display.flip()
         
        if SpaceInvaders.bullet_num() <= 0 and SpaceInvaders._spaceship._bullet == []:
            SpaceInvaders.exit_game()
    
    
    else:
        screen.blit(background, back_rect)
        SpaceInvaders.display_start_screen()
        pygame.display.flip()
        pygame.time.wait(1)



        
                





    
    
    

    
    



