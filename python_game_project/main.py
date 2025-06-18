import pygame
import random
import math
from pygame import mixer

# ***Initialise pygame, always add this line
pygame.init()

# Allows us to access code to create game screen (width and height)
# **THIS LINE WILL ALWAYS BE IN PYGAME CODES
screen = pygame.display.set_mode((800, 600))

# Add image as background
background = pygame.image.load("spacebackground.jpg")

# Background sound
pygame.mixer.init()
mixer.music.load('background.wav')
mixer.music.play(-1) # -1 means loop



# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player codes
playerIMG = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0  # setting to 0 to prepare for game movement loop



# Enemy codes
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735)) # makes sure the enemy stays on screen
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)  # 0.4 = setting to 0 to prepare for game movement loop
    enemyY_change.append(10)



# Player Bullet codes
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480 # same as playerX
bulletX_change = 0 #3   # 0.4 = setting to 0 to prepare for game movement loop
bulletY_change = 10 #40
bullet_state = "ready"  # ready state means you cannot see the bullet on the screen (fire) - bullet moving



# Score Display
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # can download fonts too www.dafont.com and download font, extract and paste file into project folder.
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True,(255, 255, 255))
    screen.blit(score, (x,y))


# Game Over Display
game_over_font = pygame.font.Font('freesansbold.ttf', 70)

def game_over_text():
    over_text = game_over_font.render("GAME OVER!", True,(255, 100, 255))
    screen.blit(over_text, (180, 250))


def player(x, y):
    # drawing players on screen
    screen.blit(playerIMG, (x, y))

def enemy(x, y, i):
    # drawing players on screen
    screen.blit(enemyIMG[i], (x, y))


# Bullet shooting function
def fire_bullet(x, y):
    global bullet_state  # initialises bullet variable state (ready, fire)
    bullet_state = "fire"
    screen.blit(bulletIMG, (x+16, y+10))  # x = bullet position, y = bullet (makes sure bullet comes from same position as spaceship)

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2))) # distance formula **
    if distance < 27:
        return True
    else:
        return False
    

# Game loop
running = True
while running:

    # Change colour of background screen
    screen.fill((255, 204, 204))
    
    # Backgroung image
    screen.blit(background, (0,0))

    # Code to exit only when X is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # If keystroke is pressed, check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4

            if event.key == pygame.K_RIGHT:
                playerX_change = 4

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play() # no -1 means only plays once
                    bulletX = playerX  # saves current position of shot bullet (doesnt move with spaceship)
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0
        
    
    # PLAYER MOVEMENT CONTROLS
    playerX += playerX_change # playerX is 5 = 5 + (left)-0.1 = 5 - 0.1 OR playerX is 5 = 5 + (right)0.5 = 5 + 0.1
    # Border control
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - 64 pixels = 736(size of spaceship png)
        playerX = 736
    


    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready" # resets bullet (ability to shoot multiple)

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    


 
     # ENEMY MOVEMENT CONTROLS
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # all enemies go below screen (hidden)
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800 - 64 pixels = 736(size of spaceship png)
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play() # no -1 means only plays once
                    
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)



    # Invokes player/ enemy method (places after screen colour so it appears on top)
    player(playerX, playerY)
    # enemy(enemyX, enemyY)
    show_score(textX, textY)


    pygame.display.update() # updates background as game events happen. ** THIS LINE WILL ALWAYS BE IN PYGAME CODE
