import pygame
import random
import math
import asyncio
import sys

pygame.init()
print("Pygame started")

#Initialize the game
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Bottle going after lemons")
clock = pygame.time.Clock()

async def main():

    #image settings
    player_image = pygame.image.load("sprite.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (50, 50))
    lemon_image = pygame.image.load("lemon.png").convert_alpha()
    lemon_image = pygame.transform.scale(lemon_image,(30, 30))

    #variables
    player_x = 50
    player_y = 300
    player_dy = 0
    gravity = 0.5
    jump_speed = -10
    on_ground = True
    running = True
    score = 0
    font = pygame.font.Font(None, 36) 
    startScore = 0
    newPlat = False

    platforms = [
        pygame.Rect(0, 350, 600, 50),
        pygame.Rect(random.randint(0, 500), random.randint(200, 300), random.randint(10, 75), 20),
        pygame.Rect(random.randint(0, 500), random.randint(60, 280), random.randint(10, 75), 20)
    ]

    class movingPlatform:
        def __init__(self, speed, yPos, width, height):
            self.speed = speed
            self.x = 0 + 20 + width / 2
            self.y = yPos
            self.width = width
            self.height = height
            self.color = (226, 141, 141)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        def move(self):
            self.x += self.speed
            if (self.x + self.width > WIDTH or self.x < 0):
                self.speed *= -1
            self.rect.x = self.x
            self.rect.y = self.y

        def draw(self):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        movingPlatform = pygame.Rect(20, random.randint(50, 100), random.randint(50, 100), 10)

    movePlat = movingPlatform(random.randint(5, 10), 
                              random.randint(100, 200),
                              random.randint(50, 70),
                              10)
    movePlat2 = movingPlatform(random.randint(5, 10), 
                              random.randint(250, 300),
                              random.randint(50, 70),
                              10)

    lemons = []
    for i in range(5):
        l1 = pygame.Rect(random.randint(50, 500), random.randint(10, 300), 30, 30)
        lemons.append(l1)

    player_rect = pygame.Rect(
        player_x,
        player_y,
        50,
        50
    )

    def newLevel():
            platforms.clear()
            newPlat1 = pygame.Rect(random.randint(0, 500), random.randint(60, 280), random.randint(10, 75), 20) 
            newPlat2 = pygame.Rect(random.randint(0, 500), random.randint(200, 300), random.randint(10, 75), 20) 
            platforms.append(pygame.Rect(0, 350, 600, 50))
            platforms.append(newPlat1)
            platforms.append(newPlat2)
        

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Keyboard controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5

        if keys[pygame.K_RIGHT]:
            player_x += 5

        if keys[pygame.K_UP] and on_ground:
            player_dy = jump_speed
            on_ground = False

        #movement
        movePlat.move()
        movePlat2.move()

        player_dy += gravity
        player_y += player_dy

        player_rect.x = player_x
        player_rect.y = player_y

        #lemon collider
        for lemon in lemons[:]:
            if player_rect.colliderect(lemon):
                lemons.remove(lemon)
                newLemon = pygame.Rect(random.randint(50, 500), random.randint(10, 300), 30, 30)
                lemons.append(newLemon)
                score += 1

        #show score
        scoreText = font.render(f"Score: {score}", True, (255, 255, 255))

        #reset the game
        if score >= startScore + 30:
            newLevel()
            startScore = score

        #collision platform
        for platform in platforms:
            if player_rect.colliderect(platform) and player_dy >= 0:
                player_rect.bottom = platform.top
                player_y = player_rect.y
                player_dy = 0
                on_ground = True
        if player_rect.colliderect(movePlat.rect) and player_dy >= 0:
                player_rect.bottom = movePlat.rect.top
                player_y = player_rect.y
                player_dy = 0
                player_x = movePlat.x
                on_ground = True
        if player_rect.colliderect(movePlat2.rect) and player_dy >= 0:
                player_rect.bottom = movePlat2.rect.top
                player_y = player_rect.y
                player_dy = 0
                player_x = movePlat2.x
                on_ground = True

        #collision floor
        if player_y >= 300:
            player_y = 300
            player_dy = 0
            on_ground = True

        #rendering
        screen.fill((0, 51, 51))
        movePlat.draw()
        movePlat2.draw()
        for platform in platforms:
            pygame.draw.rect(screen, (100, 180, 100), platform)
        for lemon in lemons:
            screen.blit(lemon_image,(lemon.x, lemon.y))
        screen.blit(player_image, (player_x, player_y))
        screen.blit(scoreText, (20, 20))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
asyncio.run(main())