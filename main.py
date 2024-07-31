import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600), display=0)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./image/rocket.png")
pygame.display.set_icon(icon)

# Background poster
background = pygame.image.load("./image/space2.jpg")
background = pygame.transform.scale(background, (800, 600))

# Background sound
mixer.music.load("./sound/background.wav")
mixer.music.play(-1)

# player
playerImg = pygame.image.load("./image/spaceship.png")
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX, playerY = 370, 500
playerX_change, playerY_change = 0, 0

# Space invaders
invadersImg = []
invaderX = []
invaderY = []
invaderX_change = []
invaderY_change = []
num_of_invaders = 6

for i in range(num_of_invaders):
    Img = pygame.image.load("./image/alien-ship.png")
    Img = pygame.transform.scale(Img, (50, 50))
    invadersImg.append(Img)
    invaderX.append(random.randint(0, 754))
    invaderY.append(random.randint(0, 400))
    invaderX_change.append(0.2)
    invaderY_change.append(10)

# Bullet, Ready --> you can't see the bullet, Fire--> bullet is currently moving
bulletImg = pygame.image.load("./image/bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (30, 30))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.3
bullet_state = "ready"

# Score
score = 0
# get more font from https://www.dafont.com/ and copy .ttf file in your code folder
font = pygame.font.Font('./font/SUNDEL.ttf', 32)
textX, textY = 10, 10

# Game over text
GO_font = pygame.font.Font('./font/Newton Howard Font.ttf', 89)

# Game creator
creater_font = pygame.font.Font('./font/Korean_Calligraphy.ttf', 32)


def show_score(x, y):
    score_ = font.render("Score : " + str(score), True, (255, 225, 255))
    screen.blit(score_, (x, y))


def game_over_text():
    GO_text = GO_font.render("Game Over", True, (255, 255, 255))
    screen.blit(GO_text, (190, 200))
    creater_text = creater_font.render("'Space Invader' game created for fun", True, (255, 255, 255))
    screen.blit(creater_text, (170, 450))


def player(x, y):
    screen.blit(playerImg, (x, y))


def invader(x, y, i):
    screen.blit(invadersImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 10))


def isCollision(invaderX, invaderY, bulletX, bulletY):
    distance = math.sqrt(math.pow(invaderX - bulletX, 2) + math.pow(invaderY - bulletY, 2))
    if distance < 50:
        print(distance)
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB
    screen.fill((90, 100, 100))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_Sound = mixer.Sound("./sound/laser.wav")
                    bullet_Sound.play()
                    # print(math.sqrt(math.pow(invaderX - bulletX, 2) + math.pow(invaderY - bulletY, 2)))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # limiting the x and y boundary
    if playerX <= 0:
        playerX = 0
    if playerX >= 754:
        playerX = 754

    # space invader movement
    for i in range(num_of_invaders):
        # game over condition
        if invaderY[i] > 400:
            for j in range(num_of_invaders):
                invaderY[j] = 2000
            game_over_text()
            break

        invaderX[i] += invaderX_change[i]
        if invaderX[i] <= 0:
            invaderX_change[i] = 0.1
            invaderY[i] += invaderY_change[i]
        if invaderX[i] >= 754:
            invaderX_change[i] = -0.1
            invaderY[i] += invaderY_change[i]

        # Collision
        collision = isCollision(invaderX[i], bulletX, invaderY[i], bulletY)
        if collision:
            explosion_Sound = mixer.Sound('./sound/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print("Invader down", score)
            invaderX[i] = random.randint(0, 754)
            invaderY[i] = random.randint(300, 400)

        invader(invaderX[i], invaderY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerX = playerX + playerX_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
