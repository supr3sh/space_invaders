import pygame
import random
import math
from pygame import mixer

#initializing and setting up the pygame
pygame.init()
screen = pygame.display.set_mode((800,600))
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invader")

#backgroud

background = pygame.image.load("background.png")

# background music

mixer.music.load("background.wav")
mixer.music.play(-1)

# score

score = 0
scoreX = 10
scoreY = 10
fontScore = pygame.font.Font('freesansbold.ttf' ,32)

def show_score(x,y):
	scoreRender = fontScore.render("SCORE : " + str(score), True, (255,255,255))
	screen.blit(scoreRender, (x,y))

# level

level = 1
levelX = 600
levelY = 10
fontLevel = pygame.font.Font('freesansbold.ttf' ,32)

def show_level(x,y):
	levelRender = fontLevel.render("LEVEL : " + str(level), True, (255,255,255))
	screen.blit(levelRender,(x,y))

# Game Over Text

over_font = pygame.font.Font('freesansbold.ttf' ,64)

def game_over_text():
	overRender = over_font.render("GAME OVER!", True, (255,255,255))
	screen.blit(overRender, (200,250))	

# bullet

bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 30
bullet_state = "ready"

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bullet ,(x+16, y+10))
	
#setting up the enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = level

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load("enemy.png"))
	enemyX.append(random.randint(0,740))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(5)
	enemyY_change.append(40)



def enemy(x,y):
	for i in range(num_of_enemies):
		screen.blit(enemyImg[i], (x[i], y[i]))
	

#setting up the player

playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
	screen.blit(playerImg, (x, y))

def isCollision(bulletX, bulletY, enemyX, enemyY):
	distance = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))
	if distance < 27:
		return True
	else:
		return False

# game loop
running = True

while(running):
	screen.fill((0,0,0))
	screen.blit(background, (0,0))
	
	# keyboard and mouse controls
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -6
			if event.key == pygame.K_RIGHT:
				playerX_change = 6
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound = mixer.Sound("laser.wav")
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
	
	# movement of player
	
	playerX += playerX_change
	
	if playerX <= 0:
		playerX = 0
	if playerX >=740:
		playerX = 740
		
	# movement of enemy
	gameOver = False
	for i in range(num_of_enemies):
		
		# Game Over
		
		if enemyY[i] > 440:
			gameOver = True
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break
		
		enemyX[i] += enemyX_change[i]
		
		if enemyX[i] <=0:
			enemyX_change[i] = 5
			enemyY[i] += enemyY_change[i]
		if enemyX[i] >=740:
			enemyX_change[i] = -5
			enemyY[i] += enemyY_change[i]
			
		
		# checking for collisions
	for i in range(num_of_enemies):
		
		if gameOver:
			break
		
		collision = isCollision(bulletX, bulletY, enemyX[i-1], enemyY[i-1])
		if collision:
			collision_sound = mixer.Sound("explosion.wav")
			collision_sound.play()
			enemyX.pop(i-1)
			enemyY.pop(i-1)
			bullet_state = "ready"
			bulletY = 480
			score += 1
			num_of_enemies -= 1

	# clearing a level
	if num_of_enemies == 0 and gameOver != True:
		level += 1
		num_of_enemies = level
		enemyImg.clear()
		enemyX.clear()
		enemyY.clear()
		enemyX_change.clear()
		enemyY_change.clear()
		
		for i in range(num_of_enemies):
			enemyImg.append(pygame.image.load("enemy.png"))
			enemyX.append(random.randint(0,740))
			enemyY.append(random.randint(50,150))
			enemyX_change.append(random.randint(2,7))
			enemyY_change.append(random.randint(30,50))
			
		
		
		enemy(enemyX, enemyY)
	else:
		enemy(enemyX, enemyY)
		
	# movement of bullet
	
	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"
	
	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change
	
	player(playerX, playerY)
	show_score(scoreX,scoreY)
	show_level(levelX,levelY)
	pygame.display.update()
