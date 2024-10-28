import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    #initiates pygame, screen size, font size for the points and for the winning font and the point
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    win_font = pygame.font.Font(None, 128)
    point = 0

    #Create different groups for the entities
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #add entities to the different groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    #spawn the asteroid field and the player
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    clock = pygame.time.Clock()
    dt = 0
    print("Starting asteroids!")
    paused = False
    check = False
    while True:
        #checks if the player has clicked the X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        if not paused:
            for updt in updatable:
                updt.update(dt)

            #checks for collision between player and asteroid
            for asteroid in asteroids:
                if asteroid.collision(player):
                    text_over = win_font.render(f"GAME OVER", True, pygame.Color('white'))
                    screen.blit(text_over, (SCREEN_WIDTH/3.5, SCREEN_HEIGHT/2.2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    sys.exit()

            #checks for collision between player shot and asteroid
            for asteroid in asteroids:
                for bullet in shots:
                    if asteroid.collision(bullet):
                        asteroid.split()
                        bullet.kill()
                        point += 1
            
            pygame.Surface.fill(screen,(0,0,0))
            
            for drawing in drawable:
                drawing.draw(screen)

            x, y = 10, 10
            text_surface = font.render(f"Current Score: {point}", True, pygame.Color('white'))
            screen.blit(text_surface, (x, y))

            #checks for the point required to win and sees check to allow endless mode
            if point == 30 and check == False:
                paused = not paused
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        
        else:
            while paused:

                #checks for player key
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            paused = not paused
                        elif event.key == pygame.K_q:
                            sys.exit()
                pygame.Surface.fill(screen,(0,0,0))

                #flips check to allow endless mode
                check = True
                
                text_win = win_font.render(f"YOU WIN!!", True, pygame.Color('white'))
                text_end = font.render(f"Please press q to exit the game or press e to go into endless!", True, pygame.Color('white'))
                screen.blit(text_win, (SCREEN_WIDTH/3, SCREEN_HEIGHT/2.2))
                screen.blit(text_end, (x, y))
                pygame.display.flip()

if __name__ == "__main__":
    main()