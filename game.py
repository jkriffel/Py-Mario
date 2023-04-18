# James Riffel
# Assignment 8
# 12/7/22
import pygame
from pygame.locals import *
from time import sleep


# Superclass Sprite contains Mario, Goomba, Pipe, Fireball, and the Floor
class Sprite:
    def __init__(self, x, y, w, h, image):
        # initialize superclass positions
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        # load the image passed through
        self.image = pygame.image.load(image)


# The model class modifies information about the sprites it contains
class Model:
    def __init__(self):
        # onFire tracks how long a goomba has been on fire
        self.onFire = 0
        # sprites array containing all sprites
        self.sprites = []
        self.sprites.append(Pipe(25, 2000, 55, 400))
        self.sprites.append(Pipe(200, 400, 55, 400))
        self.sprites.append(Pipe(500, 250, 55, 400))
        self.sprites.append(Pipe(800, 220, 55, 400))
        self.sprites.append(Pipe(1200, 220, 55, 400))
        self.sprites.append(Goomba(575, 300, 60, 60))
        self.sprites.append(Goomba(275, 400, 60, 60))
        self.sprites.append(Goomba(1000, 400, 60, 60))
        self.sprites.append(Floor(-1000, 500, 120, 10))
        self.mario = Mario(0, 100, 60, 95)
        self.sprites.append(self.mario)

    # method that adds fireball to the sprite array when left control is released
    def add_fireball(self, x, y):
        self.sprites.append(Fireball(x, y, 55, 55))

    # model update method
    def update(self):
        # nested for loops that handle the possible collisions between sprites
        for i in self.sprites:
            i.update()
            # if goomba has been on fire for long enough, remove it
            if isinstance(i, Goomba):
                if i.onFire > 20:
                    self.sprites.remove(i)
            if isinstance(i, Fireball):
                # If fireball is past the end of the game, remove it
                if i.x > 4000:
                    self.sprites.remove(i)
            # second for loop to iterate through the other sprites
            for k in self.sprites:
                # handles collision for Mario and Pipes
                if isinstance(i, Mario) and isinstance(k, Pipe):
                    if self.collision(i, k):
                        i.collide(k)
                # handles collision for Goombas and Pipes
                if isinstance(i, Goomba) and isinstance(k, Pipe):
                    if self.collision(i, k):
                        i.collidePipe(k)
                # handles collision for Goombas and Fireballs
                if isinstance(i, Goomba) and isinstance(k, Fireball):
                    if self.collision(i, k):
                        i.collide_fireball(k)
                        self.sprites.remove(k)

    # checks if collision is happening
    def collision(self, ob1, ob2):
        if ob1.x + ob2.w < ob2.x:
            return False
        if ob1.x > ob2.x + ob2.w:
            return False
        if ob1.y + ob1.h < ob2.y:
            return False
        if ob1.y > ob2.y + ob2.h:
            return False
        return True


# Subclass Mario contains mario information
class Mario(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "mario1.png")
        # Mario variables
        self.vertVelocity = 12
        self.marioCount = 0
        self.currentImage = 0
        # previous mario positions
        self.prevX = self.x
        self.prevY = self.y
        # Animation
        self.mario_images = []
        self.mario1 = pygame.image.load("mario1.png")
        self.mario2 = pygame.image.load("mario2.png")
        self.mario3 = pygame.image.load("mario3.png")
        self.mario4 = pygame.image.load("mario4.png")
        self.mario5 = pygame.image.load("mario5.png")
        # Adds animation to the array
        self.mario_images.append(self.mario1)
        self.mario_images.append(self.mario2)
        self.mario_images.append(self.mario3)
        self.mario_images.append(self.mario4)
        self.mario_images.append(self.mario5)
        self.image = self.mario_images[self.currentImage]

    def update(self):
        # tracks and updates mario physics and images
        self.image = self.mario_images[self.currentImage]
        self.marioCount += 1
        self.vertVelocity += 12
        self.y += self.vertVelocity
        # sets the floor
        if self.y > 405:
            self.vertVelocity = 0
            self.y = 405
            self.marioCount = 0
        # sets the ceiling
        if self.y < 0:
            self.y = 0

    # method that tracks previous mario position
    def lastPosition(self):
        self.prevX = self.x
        self.prevY = self.y

    # method that animates mario
    def changeImage(self):
        self.currentImage += 1
        if self.currentImage > 4:
            self.currentImage = 0

    # method that makes mario jump, called when space is pressed
    def jump(self):
        if self.marioCount == 0:
            self.vertVelocity -= 90

    # mario collision with pipes
    def collide(self, p):
        if self.x + self.w >= p.x > self.prevX + self.w:
            self.x = p.x - self.w - 1
        if self.x <= p.x + p.w < self.prevX:
            self.x = p.x + p.w + 1
        if self.y + self.h >= p.y > self.prevY + self.h:
            self.vertVelocity = 0
            self.marioCount = 0
            self.y = p.y - self.h - 1
        if self.y <= p.y + p.h < self.prevY:
            self.y = p.y + p.h + 1


# Subclass Pipe contains pipe information
class Pipe(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "pipe.png")

    def update(self):
        return True


# Subclass Floor contains floor information
class Floor(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "floor.png")

    def update(self):
        return True


# Subclass Goomba contains goomba information
class Goomba(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "goomba.png")
        # initializes goomba physics
        self.vertVelocity = 8
        self.hortVelocity = 4
        self.timer = 0
        self.currentImage = 0
        self.onFire = 0
        # tracks previous goomba position
        self.prevX = self.x
        self.prevY = self.y
        self.goombaImages = []
        self.goomba = pygame.image.load("goomba.png")
        self.goombaFire = pygame.image.load("goomba_fire.png")
        self.goombaImages.append(self.goomba)
        self.goombaImages.append(self.goombaFire)

    def update(self):
        # goomba physics and current image updating
        self.image = self.goombaImages[self.currentImage]
        self.x = self.x + self.hortVelocity
        self.vertVelocity += 14
        self.y += self.vertVelocity
        # goomba floor
        if self.y > 455:
            self.vertVelocity = 0
            self.y = 455
        # load goomba fire image and counts
        if self.currentImage == 1:
            self.onFire += 1
        return False

    # Collision between Pipes and Goombas
    def collidePipe(self, p):
        if self.x + self.w >= p.x > self.prevX + self.w:
            # self.x = p.x - self.w - 1
            self.hortVelocity = self.hortVelocity * -1
        if self.x <= p.x + p.w < self.prevX:
            # self.x = p.x + p.w + 1
            self.hortVelocity = self.hortVelocity * -1
        if self.y + self.h >= p.y > self.prevY + self.h:
            self.vertVelocity = 0
            # self.y = p.y - self.h - 1
            self.hortVelocity = self.hortVelocity * -1
        if self.y <= p.y + p.h < self.prevY:
            # self.y = p.y + p.h + 1
            self.hortVelocity = self.hortVelocity * -1

    # Collision between Fireballs and Goombas
    def collide_fireball(self, p):
        self.currentImage = 1


# Subclass Fireball contains fireball information
class Fireball(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "fireball.png")
        self.hortVelocity = 0
        self.vertVelocity = 0

    # fireball phsyics updating
    def update(self):
        self.vertVelocity += 4
        self.y += self.vertVelocity
        self.hortVelocity += 1
        self.x = self.x + self.hortVelocity
        if self.y > 455:
            self.vertVelocity -= 40
            self.x += self.vertVelocity
        return True


# View contains information about the screen
class View:
    def __init__(self, model):
        screen_size = (950, 950)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.background_image = pygame.image.load("snake.png")
        self.model = model

    def update(self):
        self.screen.fill([173, 216, 230])
        self.screen.blit(self.background_image, (0, 0))

        for sprite in self.model.sprites:
            if isinstance(sprite, Mario):
                self.screen.blit(sprite.image, (50, sprite.y))
            else:
                self.screen.blit(sprite.image, ((sprite.x - self.model.mario.x + 50), sprite.y))
        pygame.display.flip()


# Controller Class contains controller information
class Controller:
    def __init__(self, model):
        self.model = model
        self.keep_going = True

    def update(self):
        # possible key inputs are declared and initialized
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
                if event.type == K_SPACE:
                    self.keep_going = True
                if event.type == K_LCTRL:
                    self.keep_going = True
            # fireballs spawn on left control key released
            elif event.type == KEYUP:
                if event.key == K_LCTRL:
                    self.model.add_fireball(self.model.mario.x + self.model.mario.w, self.model.mario.y)
        keys = pygame.key.get_pressed()
        self.model.mario.lastPosition()
        # mario moves left and animates
        if keys[K_LEFT]:
            self.model.mario.x -= 17
            self.model.mario.changeImage()
        # mario moves right and animates
        if keys[K_RIGHT]:
            self.model.mario.x += 17
            self.model.mario.changeImage()
        #mario jumps
        if keys[K_SPACE]:
            self.model.mario.jump()


print("Use the arrow keys to move and space to jump! Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")
