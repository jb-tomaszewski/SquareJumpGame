'''
This code was largely inspired by this source:
- Author: Jon Fincher
- Date: 9/16/2019
- Type: Python code/tutorial 
- Web address: https://realpython.com/pygame-a-primer/
'''

import pygame
import random

# Import necessary user/key commands.
from pygame.locals import (
    K_SPACE,
    QUIT
)

screen_width = 500
screen_height = 500

# Use these variables for square jumping.
isJumping = False
count = 1

# This class defines the user's character, a red square.  
class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        self.surface = pygame.Surface((50, 50))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(
            center=(50, 475)
        )
        self.jumpVelocity = 7

    # Move the square based on user actions (in this case, the only user action
    # that results in user movement is the space key, which causes the square
    # to jump).
    def update(self, actions):
        # Reference the global variables used for jumping.
        global isJumping
        global count

        if actions[K_SPACE]: 
            isJumping = True

        if isJumping: 
            # Ascend until the peak of the jump is reached (based on a vertical velocity
            # of 7 pixels/count, and an acceleration of "gravity" of 1 pixel/count).
            if count <= 7:          
                self.rect.y -= int((0.5 * 1 * count ** 2) + (self.jumpVelocity * count))
                count += 1

            # Keep the square on the screen.
            if self.rect.bottom >= screen_height:
                isJumping = False
                count = 1
           
            # Descend until the square hits the bottom of the screen.
            if count > 7:
                self.rect.y += int((0.5 * 1 * count ** 2) + (self.jumpVelocity * count))
                count += 1 

        # Keep the player on the screen.
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

# This class defines an "enemy" in the game, which are small yellow squares that 
# our red square must avoid touching.  
class Enemy(pygame.sprite.Sprite):
    def __init__(self): 
        super(Enemy, self).__init__()
        self.surface = pygame.Surface((10, 10))
        self.surface.fill((255, 255, 0))
        self.rect = self.surface.get_rect(
            center=(
                random.randint(screen_width + 50, screen_width + 100),
                random.randint(425, screen_height)
            )
        )

        self.speed = 25

    # Continue to move each enemy left.  
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0: 
            self.kill()

pygame.init()

window = pygame.display.set_mode((screen_width, screen_height))

# Create unique user event for adding
# a new enemy every 800 milliseconds.  
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 800)

# Create the user's square character.
square = Square()

# Add the square and all enemies to 
# the game's group of Sprites.  
enemies = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
allSprites.add(square)

windowOpen = True

while windowOpen: 
    # Slight time delay allows for more smoothness with movements.
    pygame.time.delay(50)

    # Check if the user wants to quit the game, or if a new enemy 
    # should be added to the screen.
    for event in pygame.event.get(): 
        if event.type == QUIT:
            windowOpen = False

        elif event.type == ADDENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            allSprites.add(enemy)

    # See if the user wants the square to jump.
    actions = pygame.key.get_pressed()
    square.update(actions)

    # Keep moving enemies to the left.
    enemies.update()

    # Fill the window with a black background.
    window.fill((0, 0, 0))

    # Put all Sprites (the user's square and any enemies)
    # on the screen.
    for sprite in allSprites:
        window.blit(sprite.surface, sprite.rect)

    # If the user's square collides with an enemy, 
    # end the game.  
    if pygame.sprite.spritecollideany(square, enemies): 
        square.kill()
        windowOpen = False

    # Update the screen.
    pygame.display.flip()