import player
from shapely.geometry import Polygon
import pygame
import math
import time
import threading
from random import randint

class game:

    background_color = (0, 0 ,0)
    start = 0
    font = ""
    clock = 0
    done = False
    player_is_dead = False
    screen = ""
    pygame = ""
    t = 0.01
    gravity = 9800
    jump_speed = -1500

    player_size = (60,60)
    spike_color = (125, 125, 125)
    spike_width = 100
    spike_height = 50

    spike_arr = []
    level = 1

    player1 = ""
    player2 = ""
    screen_size = (0, 0)

    def __init__(self, pygame, screen):

        self.pygame = pygame
        self.screen = screen
        self.start = time.time()
        self.font = pygame.font.SysFont('Comic Sans MS', 72)
        self.clock = pygame.time.Clock()
        self.screen_size = pygame.display.get_surface().get_size()

        self.player1 = player.player((0,100), 5, (0,255,0), "Player 1")
        self.player2 = player.player((self.screen_size[0] - self.player_size[0], 100), -5, (0,0,255), "Player 2")
        self.launch()

    def launch(self):

        while not self.done:

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_x]:
                self.game_reset()

            time.sleep(self.t)
            self.screen.fill(self.background_color)
            self.draw_spikes()
            self.draw_level()

            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.done = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                if not self.player1.is_press:
                    self.player1.vely = self.jump_speed
                    self.player1.jump = True
                    self.player1.is_press = True
                else:
                    self.player1.is_press = False
            
            if pressed[pygame.K_w]:
                if not self.player2.is_press:
                    self.player2.vely = self.jump_speed
                    self.player2.jump = True
                    self.player2.is_press = True
                else:
                    self.player2.is_press = False

            if not self.player_is_dead:
                self.set_y_value(self.player1)
                self.set_y_value(self.player2)
                
                self.adjust_velx(self.player1)     
                self.adjust_velx(self.player2)
                
            self.is_player_alive(self.player1)
            self.is_player_alive(self.player2)

            self.pygame.draw.rect(self.screen, self.player1.color, self.pygame.Rect(self.player1.x, self.player1.y, self.player_size[0], self.player_size[1]))
            self.pygame.draw.rect(self.screen, self.player2.color, self.pygame.Rect(self.player2.x, self.player2.y, self.player_size[0], self.player_size[1]))

            self.pygame.display.flip()
            self.clock.tick(60)

    def draw_level(self):
        level_txt = self.font.render(str(self.level), False, (0, 255, 0))
        self.screen.blit(level_txt, ((self.screen_size[0] / 2 ) - (level_txt.get_width()/2), 50))
            
    def set_y_value(self, player):

        player.vely = player.vely + self.gravity * self.t
        player.y = player.y + player.vely * self.t

    def adjust_velx(self, player):

        if player.x < 0 or player.x > 940:
            player.velx *= -1
            d = threading.Thread(name='gen_spike', target=self.gen_spikes)
            d.start()
            
        if player.x < 0:
            self.level += 1

        player.x += player.velx

    def draw_spikes(self):

        sw = self.spike_width
        sh = self.spike_height
        w = self.screen_size[0]
        h = self.screen_size[1]

        for i in xrange(1, w, sw):
            self.pygame.draw.polygon(self.screen, self.spike_color,[[i,0],[i + sw/2, sh],[i + sw,0]], 0)
            self.pygame.draw.polygon(self.screen, self.spike_color,[[i,h],[i + sw/2, h - sh],[i + sw,h]], 0)

        for c in self.spike_arr:
            self.pygame.draw.polygon(self.screen, self.spike_color, [c[0], c[1], c[2]], 0)
            
    def gen_spikes(self):

        time.sleep(0.5)
        sw = self.spike_width
        sh = self.spike_height
        w = self.screen_size[0]
        h = self.screen_size[1]

        r = randint(1, 255)
        g = randint(1, 255)
        b = randint(1, 255)
        self.spike_color = (r, g, b)

        max_val = (self.screen_size[1] / self.spike_width) - 3
        r = randint(1, max_val)
        self.spike_arr = []

        while len(self.spike_arr) < r:
            b = randint(1, max_val) * self.spike_width
            while b in self.spike_arr:
                b = randint(1, max_val) * self.spike_width
            self.spike_arr.append([(0,b),(sh, b + sw/2),(0,b + sw)])
            self.spike_arr.append([(w,b),(w - sh, b + sw/2),(w,b + sw)])

    def game_reset(self):
        self.player1 = player.player((0,100), 5, (0,255,0), "Player 1")
        self.player2 = player.player((self.screen_size[0] - self.player_size[0], 100), -5, (0,0,255), "Player 2")
        self.player_is_dead = False
        self.level = 1
        self.spike_arr = []

    def is_player_alive(self, player):
        if not self.spike_height < player.y < self.screen_size[1] - self.spike_height - self.player_size[1]:
            textsurface = self.font.render(player.name + ' DIED', False, (255, 0, 0))
            self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2), (self.screen_size[1] / 2) - (textsurface.get_height()/2)))
            self.player_is_dead = True
        
        p = Polygon([(player.x, player.y),(player.x, player.y + self.player_size[1]),(player.x + self.player_size[0], player.y + self.player_size[1]),(player.x + self.player_size[0], player.y)])
        
        for c in self.spike_arr:
            s = Polygon(c)
            if p.intersects(s):
                textsurface = self.font.render(player.name + ' DIED', False, (255, 0, 0))
                self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2), (self.screen_size[1] / 2) - (textsurface.get_height()/2)))
                self.player_is_dead = True