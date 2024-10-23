import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    win_font = pygame.font.Font(None, 128)
    point = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    clock = pygame.time.Clock()
    dt = 0
    print("Starting asteroids!")
    paused = False
    check = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        if not paused:
            for updt in updatable:
                updt.update(dt)

            for asteroid in asteroids:
                if asteroid.collision(player):
                    print("Game over!")
                    sys.exit()

            for asteroid in asteroids:
                for bullet in shots:
                    if asteroid.collision(bullet):
                        asteroid.kill()
                        bullet.kill()
                        point += 1
            
            pygame.Surface.fill(screen,(0,0,0))
            
            for drawing in drawable:
                drawing.draw(screen)

            x, y = 10, 10
            text_surface = font.render(f"Current Score: {point}", True, pygame.Color('white'))
            screen.blit(text_surface, (x, y))

            if point == 10 and check == False:
                paused = not paused
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        
        else:
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            paused = not paused
                pygame.Surface.fill(screen,(0,0,0))
                check = True
                text_win = win_font.render(f"YOU WIN!!", True, pygame.Color('white'))
                text_end = font.render(f"Please exit the game or press e to go into endless!", True, pygame.Color('white'))
                screen.blit(text_win, (SCREEN_WIDTH/3, SCREEN_HEIGHT/2.2))
                screen.blit(text_end, (x, y))
                pygame.display.flip()

if __name__ == "__main__":
    main()