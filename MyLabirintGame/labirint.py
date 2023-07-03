# Разработай свою игру в это
from pygame import *
init()
font1 = font.SysFont('verdana', 30)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
win_back = transform.scale(image.load('stonks.jpg'), (700, 500))
win_text = font.SysFont('verdana', 60).render('YOU WON!!!', True, (255, 255, 255))
lose_back = transform.scale(image.load('gameover.jpg'), (700, 500))
display.set_caption('Моя первая игра')
run = True

class GameSprite(sprite.Sprite):
    def __init__(self, width, height, x, y, picture):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, width, height, x, y, picture, x_speed, y_speed):
        super().__init__(width, height, x, y, picture)
        self.x_speed = x_speed
        self.y_speed = y_speed
        

    def update(self):
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.rect.x <= win_width - self.rect.width and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        if self.x_speed > 0:
            for platform in platforms_touched:
                self.x_speed = 0
                self.rect.right = min(self.rect.right, platform.rect.left)    
        elif self.x_speed < 0:
            for platform in platforms_touched:
                self.x_speed = 0
                self.rect.left = max(self.rect.left, platform.rect.right)
        if self.rect.y <= win_height - self.rect.height and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:    
            self.rect.y += self.y_speed        
        if self.y_speed > 0:
            for platform in platforms_touched:
                self.y_speed = 0
                self.rect.bottom = min(self.rect.bottom, platform.rect.top)
        elif self.y_speed < 0:
            for platform in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, platform.rect.bottom)

class Enemy(GameSprite):
    side = ''
    initial_point = ()
    def __init__(self, width, height, x, y, picture, speed, distance, axis):
        super().__init__(width, height, x, y, picture)
        self.initial_point = (x, y)
        self.speed = speed
        self.distance = distance
        self.axis = axis
        if self.axis == 'x':
            self.side = 'left'
        else:
            self.side = 'top'

    def update(self):
        if self.axis == 'x':
            if self.initial_point[0] >= self.rect.x:
                self.side = 'right'
            elif self.initial_point[0] + self.distance <= self.rect.x:
                self.side = 'left'
            if self.side == 'right':
                self.rect.x += self.speed
            elif self.side == 'left':
                self.rect.x -= self.speed
        elif self.axis == 'y':
            if self.initial_point[1] >= self.rect.y:
                self.side = 'down'
            elif self.initial_point[1] + self.distance <= self.rect.y:
                self.side = 'up'
            if self.side == 'down':
                self.rect.y += self.speed
            elif self.side == 'up':
                self.rect.y -= self.speed
            
class Bullet(GameSprite):
    def __init__(self, width, height, x, y, picture, speed):
        super().__init__(width, height, x, y, picture)
        self.speed = speed
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.kill()
            print('bullet killed')

barriers = sprite.Group()
walls = [
        GameSprite(25, 300, 25, 0, 'wall.png'), 
        GameSprite(200, 25, 100, 275, 'wall.png'), 
        GameSprite(25, 100, 300, 275, 'wall.png'), 
        GameSprite(100, 25, 325, 350, 'wall.png'),
        GameSprite(25, 200, 400, 100, 'wall.png')
        ]




for wall in walls:
    barriers.add(wall)
player = Player(30, 45, 5, 415, 'man.png', 0, 0)
enemy_list = [Enemy(30, 45, 595, 385, 'owtlaw.png', 5, 100, 'x'), Enemy(30, 45, 425, 200, 'owtlaw.png', 5, 100, 'y')]
enemies = sprite.Group()
for enemy in enemy_list:
    enemies.add(enemy)
suitcase = GameSprite(50, 50, 595, 0, 'suitcase.png')
bullets = sprite.Group()

finish = False
win = False
lose = False

while run:
    time.delay(50)
    window.fill((255, 255, 255))

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -5
            elif e.key == K_DOWN:
                player.y_speed = 5
            elif e.key == K_RIGHT:
                player.x_speed = 5
            elif e.key == K_LEFT:
                player.x_speed = -5
        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_LEFT:
                player.x_speed = 0
    
    if sprite.collide_rect(player, suitcase):
        win = True
    elif sprite.collide_rect(player, enemy):
        lose = True
    
    if win or lose:
        finish = True 

    if finish != True:
        barriers.draw(window)
        enemies.draw(window)
        for enemy in enemies:
            enemy.update()
        suitcase.reset()
        player.reset()
        player.update()
        for enemy in enemies:    
            if player.rect.x + player.rect.width / 2 == enemy.rect.x:
                bullets.add(Bullet(10, 20, enemy.rect.x, enemy.rect.y, 'bullet.png', 5))
            for bullet in bullets:
                bullet.update()
                if sprite.collide_rect(player, bullet):
                    lose = True
            bullets.draw(window)
    else:
        if win:
            window.blit(win_back, (0, 0))
            window.blit(win_text, (175, 200))
        elif lose:
            window.blit(lose_back, (0, 0))
    display.update()


