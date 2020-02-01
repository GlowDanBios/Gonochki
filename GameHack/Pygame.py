import pygame
import sys
import random
import time
from pygame.transform import scale

def mainmenu():
    #menu
    pygame.font.init()
    window = pygame.display.set_mode((1280, 1024))
    pygame.display.set_caption('Race Runner 2020')
    menu = pygame.Surface((1280, 1024))
    screen = pygame.Surface((1280, 1024))
    img = pygame.image.load('car.png').convert_alpha()
    menu_img = scale(pygame.image.load('background.png').convert_alpha(),(1280,1024))
    pygame.display.set_icon(img)


    class Menu:
        def __init__(self, captions, punkts=[(400, 350, u'Punkt', (250, 250, 30), (250, 30, 250))]):
            self.captions = captions
            self.punkts = punkts

        def render(self, poverhnost, num_punkt, p):
            punkts = p
            for i in punkts:
                font = pygame.font.Font(i[6][0], i[6][1])
                if num_punkt == i[5]:
                    poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
                else:
                    poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

        def menu(self):
            done = True
            font_menu = pygame.font.Font(None, 300)
            pygame.key.set_repeat(0, 0)
            pygame.mouse.set_visible(True)
            punkt = 0
            menu.blit(menu_img,(0,0))
            screen.blit(menu_img,(0,0))
            self.render(screen, 2, self.captions)
            while done:


                mp = pygame.mouse.get_pos()
                for i in self.punkts:
                    if mp[0] > i[0] and mp[0] < i[0] + 255 and mp[1] > i[1] and mp[1] < i[1] + 150:
                        punkt = i[5]
                self.render(screen, punkt, self.punkts)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            sys.exit()
                        if e.key == pygame.K_UP:
                            if punkt > 0:
                                punkt -= 1
                        if e.key == pygame.K_DOWN:
                            if punkt < len(self.punkts) - 1:
                                punkt += 1
                        if e.key == pygame.K_1:
                            if punkt == 0:
                                done = False
                            elif punkt == 1:
                                exit()
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        if punkt == 0:
                            done = False
                        elif punkt == 1:
                            exit()
                window.blit(menu, (0, 0))
                window.blit(screen, (0, 30))
                pygame.display.flip()
                pygame.time.delay(5)


    punkts = [(170, 180, u'Play', (11, 0, 77), (250, 250, 30), 0, ('18347.ttf', 200)),
              (170, 400, u'Exit', (11, 0, 77), (250, 250, 30), 1, ('18347.ttf', 200))]
    captions = [(70, 50, u'Race Runner 2020', (11, 0, 77), (250, 250, 30), 0, ('18347.ttf',100))]
    game = Menu(captions, punkts)
    game.menu()

def main():
    #-----------------------------------------------------------------------------------------------------------------------
    #game

    pygame.init()
    # background
    gameover = scale(pygame.image.load('go.png'),(1280+100,1024+100))
    screen = pygame.display.set_mode((1280,1024))
    bg =scale(pygame.image.load('doroga1.jpg').convert_alpha(),(1280,1024))
    screen.blit(bg, (0, 0))
    screen.set_alpha(None)

    # icon
    img = pygame.image.load('car.png').convert_alpha()
    pygame.display.set_icon(img)

    #pictures
    img_rock = scale(pygame.image.load("rock.png").convert_alpha(),(100,200))
    img_bush = scale(pygame.image.load("bush.png").convert_alpha(),(100,200))
    img_box = scale(pygame.image.load("box.png").convert_alpha(),(100,200))
    img_coin = scale(pygame.image.load('coin.png').convert_alpha(),(75, 75))
    # fps
    clock = pygame.time.Clock()
    pygame.display.update()

    #soundtrack
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    sound = pygame.mixer.Sound('gameover.wav')


    # constants classes and functions
    class Coins(pygame.sprite.Sprite):
         def __init__(self,x,y,speed):
             pygame.sprite.Sprite.__init__(self)
             self.image = img_coin
             self.rect = pygame.Rect(x, y, 50, 50)
             self.yvel = speed

         def draw(self, screen):
             screen.blit(self.image, (self.rect.x, self.rect.y))

         def update(self):
             self.rect.y += self.yvel

             if self.rect.y > 1000:
                 self.kill()

             for block in blocks:
                 if self.rect.colliderect(block.rect):
                     self.kill()



    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 40, 40)
            self.images = []
            self.index = 0

            for i in range(8):
                image = scale(pygame.image.load("tile00{}.png".format(i)).convert_alpha(), (100, 100))
                self.images.append(image)

        def draw(self, screen):
            if self.index < 8:
                screen.blit(self.images[self.index], (self.rect.x, self.rect.y))
                self.index += 1


    class Bushes(pygame.sprite.Sprite):
        def __init__(self, x, y, speed):
            pygame.sprite.Sprite.__init__(self)
            imgs = [img_box, img_bush,img_rock]
            self.image = scale(random.choice(imgs), (100, 100))
            self.rect = pygame.Rect(x, y, 70, 70)
            self.yvel = speed

        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

        def update(self):
            self.rect.y += self.yvel

            if self.rect.y > 1000:
                self.kill()

    x = 5
    class Car(pygame.sprite.Sprite):
        def __init__(self, x, y,img):
            pygame.sprite.Sprite.__init__(self)
            self.img_car = [pygame.image.load(img).convert_alpha(),pygame.image.load('car_left.png').convert_alpha(),pygame.image.load('car_right.png').convert_alpha()]
            self.img_car2 = [pygame.image.load(img).convert_alpha(), pygame.image.load('car2_left.png').convert_alpha(), pygame.image.load('car2_right.png').convert_alpha()]
            self.rect = pygame.Rect(x, y, 50, 100)
            self.image = scale(pygame.image.load(img).convert_alpha(), (75, 150)).convert_alpha()
            self.xvel = 0
            self.yvel = 0
            self.life = 5
            self.dead = False
            self.score = 0
            self.explosions = []

        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

            for explosion in self.explosions:
                explosion.draw(screen)

        def update(self, left, right, up, down, asteroids):
            if left:
                if self.rect.x < 80:
                    if self == car:
                        self.image = scale(self.img_car[0], (75, 150))
                    else:
                        self.image = scale(self.img_car2[0],(75, 150))
                    self.xvel = 0
                else:
                    if self == car:
                        self.image = scale(self.img_car[1], (75, 150))
                    else:
                        self.image = scale(self.img_car2[1], (75, 150))
                    self.xvel = -5

            if right:
                if self.rect.x > 1133:
                    if self == car:
                        self.image = scale(self.img_car[0], (75, 150))
                    else:
                        self.image = scale(self.img_car2[0], (75, 150))
                    self.xvel = 0
                else:
                    if self == car:
                        self.image = scale(self.img_car[2], (75, 150))
                    else:
                        self.image = scale(self.img_car2[2], (75, 150))
                    self.xvel = 5

            if up:
                if self.rect.y < 80:
                    self.yvel = 0
                else:
                    self.yvel = -5

            if down:
                if self.rect.y > 703:
                    self.yvel = 0
                else:
                    self.yvel = 5

            if not (left or right or up or down):
                self.xvel = 0
                if self == car:
                    self.image = scale(self.img_car[0], (75, 150))
                else:
                    self.image = scale(self.img_car2[0], (75, 150))
                if self.rect.y > 703:
                    self.yvel = 0
                else:
                    self.yvel = 3
            self.rect.x += self.xvel
            self.rect.y += self.yvel

            for block in blocks:
                if self.life == 0:
                    self.dead = True
                elif self.rect.colliderect(block.rect):
                    self.life -= 1
                    rx = random.randint(-5, 40)
                    ry = random.randint(-5, 40)
                    explosion = Explosion(self.rect.x + rx, self.rect.y + ry)
                    self.explosions.append(explosion)
                    block.kill()
            for coin in coins:
                if self.rect.colliderect(coin.rect):
                    coin.kill()
                    self.score += 300



    car = Car(200, 750, 'car.png')
    car2 = Car(643, 750, 'car2.png')
    speed = 10
    left = False
    right = False
    up = False
    down = False
    left2 = False
    right2 = False
    up2 = False
    down2 = False
    coins =  pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    f =0
    f2 = -1024

    # main game
    while True:
        clock.tick(80)
        screen.blit(bg, (0, f))
        screen.blit(bg, (0, f2))
        if (car.score%1000 == 0) or (car2.score%1000 == 0):
            speed += 2
        f +=  speed
        f2 +=  speed
        if f > 1000:
            f = -1024
        if f2 > 1000:
            f2 = -1024
        if random.randint(1, 1000) > 960:
            block_x = random.randint(90, 1120)
            block_y = -10
            block = Bushes(block_x, block_y,speed)
            blocks.add(block)
        if random.randint(1, 1000) > 990:
            coin_x = random.randint(90, 920)
            coin_y = -10
            coin = Coins(coin_x, coin_y,speed)
            coins.add(coin)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                left = True
                right = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                right = True
                left = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_w:
                up = True
                down = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                down = True
                up = False

            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left2 = True
                right2 = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right2 = True
                left2 = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up2 = True
                down2 = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                down2 = True
                up2 = False

            if e.type == pygame.KEYUP and e.key == pygame.K_a:
                left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_d:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_w:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_s:
                down = False

            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left2 = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right2 = False
            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up2 = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                down2 = False

            elif e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not car.dead:
            car.score += 1
            car.update(left, right, up, down, blocks)
            car.draw(screen)
        if not car2.dead:
            car2.score += 1
            car2.update(left2, right2, up2, down2, blocks)
            car2.draw(screen)

        for block in blocks:
            block.update()
            block.draw(screen)

        for coin in coins:
            coin.update()
            coin.draw(screen)

        life = font.render('RED_LIFE: {}'.format(car.life), False, (0, 255, 255))
        life2 = font.render('BLUE_LIFE: {}'.format(car2.life), False, (0, 255, 255))
        score = font.render('RED_SCORE: {}'.format(car.score), False, (0, 255, 255))
        score2 = font.render('BLUE_SCORE: {}'.format(car2.score), False, (0, 255, 255))

        if car.dead and car2.dead:
            pygame.mixer.music.stop()
            screen.blit(gameover,(-100,-100))
            sound.play()
            if car.score > car2.score:
                screen.blit(score, (500, 800))
                screen.blit(score2, (500, 900))
            else:
                screen.blit(score2, (500, 900))
                screen.blit(score, (500, 800))

            pygame.display.update()
            time.sleep(5)
            break
            # pygame.quit()
        else:
            screen.blit(life , (20, 20))
            screen.blit(life2, (820, 20))
            screen.blit(score, (20, 60))
            screen.blit(score2, (820, 60))


        pygame.display.update()


while True:
    mainmenu()
    main()
