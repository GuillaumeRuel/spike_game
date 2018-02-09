import game
import pygame
import math
import time

class main:

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    game = game.game(screen, 1920, 1080)


if __name__ == "__main__":
    main()

