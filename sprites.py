# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(257, 44, 80, 72),
                                self.game.spritesheet.get_image(257, 44, 80, 72)]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)
        self.walk_frames_l = [self.game.spritesheet.get_image(27, 313, 70, 80),
                              self.game.spritesheet.get_image(99, 310, 69, 80)]
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            frame.set_colorkey(WHITE)
            self.walk_frames_r.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(WHITE)

        self.stand_flip = pg.transform.flip(self.standing_frames[0], True, False)


    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction = 1
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.direction = 0
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
            self.rect.midbottom = self.pos
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x > 1 or self.vel.x < -1:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                    self.direction = 0
                else:
                    self.direction = 1
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                if self.direction:
                    self.image = self.standing_frames[self.current_frame]
                else:
                    self.image = self.stand_flip
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.image = self.game.spritesheet.get_image(29, 123, 85, 20)
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, (150, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spritesheet:
    # utility class for loading sprite sheets
    def __init__(self, filename):
        self.sprite_sheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab image
        image = pg.Surface((width,height))
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        return image


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load('tf.jpg')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

