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

    spike_color = (125, 125, 125)
    spike_width = 100
    spike_height = 50

    spike_arr = []
    static_spike_arr = []
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

        self.player1 = player.player((0,150), 5, (0,255,0), "Player 1")
        self.player2 = player.player((self.screen_size[0] - self.player1.width, 150), -5, (0,0,255), "Player 2")

        self.gen_static_spike()
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
                if not self.player1.in_action:
                    self.player1.jump()
                else:
                    self.player1.in_action = False
            
            if pressed[pygame.K_w]:
                if not self.player2.in_action:
                    self.player2.jump()
                else:
                    self.player2.in_action = False

            #check if the player 1 touch the edge
            if self.player1.x < 0 or self.player1.x > self.screen_size[0] - self.player1.width:
                d = threading.Thread(name='gen_spike', target=self.gen_spikes)
                d.start()
                self.level += 1

            self.is_player_alive(self.player1)
            self.is_player_alive(self.player2)

            if not self.player_is_dead:
                self.update_player(self.player1)
                self.update_player(self.player2)

            self.pygame.draw.rect(self.screen, self.player1.color, self.pygame.Rect(self.player1.x, self.player1.y, self.player1.width, self.player1.height))
            self.pygame.draw.rect(self.screen, self.player2.color, self.pygame.Rect(self.player2.x, self.player2.y, self.player2.width, self.player2.height))

            self.pygame.display.flip()
            self.clock.tick(60)
    
    def update_player(self, player):
        player.update_y_velocity(self.t)
        player.update_y_position(self.t)
        player.update_x_position(self.screen_size[0])

    def draw_level(self):
        level_txt = self.font.render(str(self.level), False, (0, 255, 0))
        self.screen.blit(level_txt, ((self.screen_size[0] / 2 ) - (level_txt.get_width()/2), 50))
    
    def draw_end_game_msg(self):
        textsurface = self.font.render(player.name + ' lost!', False, (255, 0, 0))
        self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2), (self.screen_size[1] / 2) - (textsurface.get_height()/2)))

    def draw_spikes(self):
        for c in self.spike_arr:
            self.pygame.draw.polygon(self.screen, self.spike_color, [c[0], c[1], c[2]], 0)
        for c in self.static_spike_arr:
            self.pygame.draw.polygon(self.screen, self.spike_color, [c[0], c[1], c[2]], 0)

    def gen_static_spike(self):
        width = self.screen_size[0]
        height = self.screen_size[1]

        for i in xrange(1, width, self.spike_width):
            self.static_spike_arr.append([(i,0),(i + self.spike_width/2, self.spike_height),(i + self.spike_width, 0)])
            self.static_spike_arr.append([(i,height),(i + self.spike_width/2, height - self.spike_height),(i + self.spike_width, height)])
            
    def gen_spikes(self):
        time.sleep(0.5)
        w = self.screen_size[0]
        h = self.screen_size[1]

        self.random_spike_color()

        max_val = (self.screen_size[1] / self.spike_width) - 3
        r = randint(1, max_val)
        self.spike_arr = []

        while len(self.spike_arr) < r :
            b = randint(1, max_val) * self.spike_width
            while b in self.spike_arr:
                b = randint(1, max_val) * self.spike_width
            self.spike_arr.append([(0,b),(self.spike_height, b + self.spike_width/2),(0,b + self.spike_width)])
            self.spike_arr.append([(w,b),(w - self.spike_height, b + self.spike_width/2),(w,b + self.spike_width)])
    
    def random_spike_color(self):
        r = randint(50, 175)
        g = randint(50, 175)
        b = randint(50, 175)
        self.spike_color = (r, g, b)

    def game_reset(self):
        self.player1 = player.player((0,100), 5, (0,255,0), "Player 1")
        self.player2 = player.player((self.screen_size[0] - self.player1.width, 100), -5, (0,0,255), "Player 2")
        self.player_is_dead = False
        self.level = 1
        self.spike_arr = []
        self.gen_static_spike()

    def is_player_alive(self, player):        
        p = Polygon(player.get_polygon())

        for c in self.static_spike_arr:
            s = Polygon(c)
            if p.intersects(s):
                self.player_is_dead = True
        
        for c in self.spike_arr:
            s = Polygon(c)
            if p.intersects(s):
                self.player_is_dead = True

        if self.player_is_dead:
            self.draw_end_game_msg()
                