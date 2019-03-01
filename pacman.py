import pygame
from pygame.locals import *
from numpy import loadtxt
import time
import random

pygame.init()
#Constants for the game
WIDTH, HEIGHT = (32, 32)
WALL_COLOR = pygame.Color(0, 0, 255, 255) # BLUE
PACMAN_COLOR = pygame.Color(255, 0, 0, 255) # RED
COIN_COLOR = pygame.Color(255, 255, 0, 255) # RED
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
score=0
aniCount=0
# FPS=60
# fpsClock=pygame.time.Clock()
myfont = pygame.font.Font('ARCADE_N.TTF', 20)
myfont1 = pygame.font.Font('ARCADE_N.TTF', 24)
myfontTitle = pygame.font.Font('ARCADE_N.TTF', 60)
startTime=time.time()
lives=3

#makes a list of images
pmanRight = [pygame.image.load('sprites/pacman/pacman3right.png'), pygame.image.load('sprites/pacman/pacman2right.png'), pygame.image.load('sprites/pacman/pacman1right.png')]
pmanLeft = [pygame.image.load('sprites/pacman/pacman3left.png'), pygame.image.load('sprites/pacman/pacman2left.png'), pygame.image.load('sprites/pacman/pacman1left.png')]
pmanUp = [pygame.image.load('sprites/pacman/pacman3up.png'), pygame.image.load('sprites/pacman/pacman2up.png'), pygame.image.load('sprites/pacman/pacman1up.png')]
pmanDown = [pygame.image.load('sprites/pacman/pacman3down.png'), pygame.image.load('sprites/pacman/pacman2down.png'), pygame.image.load('sprites/pacman/pacman1down.png')]

# pman = pygame.image.load('sprites/pacman/pacman2right.png')

wallbackground=pygame.image.load('background.png')
black=pygame.image.load('black.png')

blinky = [pygame.image.load('sprites/ghosts/blinkyUp.png'), pygame.image.load('sprites/ghosts/blinkyDown.png'), pygame.image.load('sprites/ghosts/blinkyLeft.png'), pygame.image.load('sprites/ghosts/blinkyRight.png')]
inky = [pygame.image.load('sprites/ghosts/inkyUp.png'), pygame.image.load('sprites/ghosts/inkyDown.png'), pygame.image.load('sprites/ghosts/inkyLeft.png'), pygame.image.load('sprites/ghosts/inkyRight.png')]
pinky = [pygame.image.load('sprites/ghosts/pinkyUp.png'), pygame.image.load('sprites/ghosts/pinkyDown.png'), pygame.image.load('sprites/ghosts/pinkyLeft.png'), pygame.image.load('sprites/ghosts/pinkyRight.png')]
clyde = [pygame.image.load('sprites/ghosts/clydeUp.png'), pygame.image.load('sprites/ghosts/clydeDown.png'), pygame.image.load('sprites/ghosts/clydeLeft.png'), pygame.image.load('sprites/ghosts/clydeRight.png')]

blue=pygame.image.load('sprites/ghosts/blue.png')
menuImg = pygame.image.load('menu.png')


def translucentLayer(screen,pos):
	pixels = pixels_from_points(pos)
	translucent = pygame.Surface((672,640))
	translucent.set_alpha(164)
	translucent.fill((0,0,0))
	# pygame.draw.rect(translucent, (0,0,0), [(0,0), (672, 640)])
	screen.blit(translucent, (0,0))

#Draws a rectangle for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	# screen.blit(wall,pixels)
	pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])

def draw_pacman(screen, pos): 
	global aniCount
	pixels = pixels_from_points(pos)

	if aniCount + 1 >= 6: #limits the 3 images of sprites to 15 fps
		aniCount = 0

	if rightDir:
		screen.blit(pmanRight[aniCount//2],pixels) #change image after 5th iteration
		aniCount+=1
	
	if leftDir:
		# pman=pygame.transform.rotate(pman[aniCount//3],180)
		screen.blit(pmanLeft[aniCount//2],pixels) #change image after 5th iteration
		aniCount+=1

	if upDir:
		# pman=pygame.transform.rotate(pman[aniCount//3],90)
		screen.blit(pmanUp[aniCount//2],pixels) #change image after 5th iteration
		aniCount+=1

	if downDir:
		# pman=pygame.transform.rotate(pman[aniCount//3],-90)
		screen.blit(pmanDown[aniCount//2],pixels) #change image after 5th iteration
		aniCount+=1

	# pygame.draw.rect(screen, PACMAN_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the coin
def draw_coin(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.circle(screen, COIN_COLOR, (pixels[0]+16,pixels[1]+16), 4)

#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)


class ghost:

	def __init__(self, ghostName, ghost_position, ghost_direction, eyeDir):

		self.ghostName=ghostName
		self.ghost_position=ghost_position
		self.ghost_direction=ghost_direction
		self.eyeDir=eyeDir

	def random(self):

		if (self.ghost_position[0]>4 and self.ghost_position[1]>8 and self.ghost_position[0]<16 and self.ghost_position[1]<11):
			if self.ghost_position[0]<10:
				self.ghost_direction = RIGHT
				self.eyeDir = 3
			if self.ghost_position[0]>10:
				self.ghost_direction = LEFT
				self.eyeDir = 2
			else:
				self.ghost_direction = TOP

		else:

			if float(round(self.ghost_position[0],2)).is_integer() and float(round(self.ghost_position[1],2)).is_integer(): #only runs if it's an interer position

				possible=[] #list that will have possible routes at an intersection

				if layout[round(self.ghost_position[1])-1][round(self.ghost_position[0])] != 'w': #if no wall at top, it's a possible route
					possible.append(TOP)
				if layout[round(self.ghost_position[1])+1][round(self.ghost_position[0])] != 'w': #if no wall at down, it's a possible route
					possible.append(DOWN)
				if layout[round(self.ghost_position[1])][round(self.ghost_position[0])-1] != 'w': #if no wall at left, it's a possible route
					possible.append(LEFT)
				if layout[round(self.ghost_position[1])][round(self.ghost_position[0])+1] != 'w': #if no wall at right, it's a possible route
					possible.append(RIGHT)
				

				if self.ghost_direction == TOP:
					possible.remove(DOWN) #remove down if top is possible solution
				if self.ghost_direction == DOWN:
					possible.remove(TOP) #remove top if down is possible solution
				if self.ghost_direction == LEFT:
					possible.remove(RIGHT) #remove right if left is possible solution
				if self.ghost_direction == RIGHT:
					possible.remove(LEFT) #remove left if right is possible solution


				self.ghost_direction=random.choice(possible)

			if self.ghost_direction == TOP:
				self.eyeDir=0
			if self.ghost_direction == DOWN:
				self.eyeDir=1
			if self.ghost_direction == LEFT:
				self.eyeDir=2
			if self.ghost_direction == RIGHT:
				self.eyeDir=3


		if (round(self.ghost_position[0]),round(self.ghost_position[1]))==(-1,9) and self.ghost_direction==LEFT:
			self.ghost_position=(21,9) #For left portal

		if (round(self.ghost_position[0]),round(self.ghost_position[1]))==(21,9) and self.ghost_direction==RIGHT:
			self.ghost_position=(-1,9) #For right portal

	def reset(self):

		self.ghost_position = (10,10)
		self.ghost_direction = (0,0)
		self.eyeDir = 0

	def draw_ghost(self):
		pixels = pixels_from_points(self.ghost_position)
		# pygame.draw.rect(screen, (255,0,0), [pixels, (WIDTH, HEIGHT)])
		# pygame.draw.circle(screen, (255,0,0), (int(pixels[0]+16),int(pixels[1])+16), 8)
		screen.blit(self.ghostName[self.eyeDir],pixels)


	def intersect(self):

		global pacman_position, move_direction, lives
		
		if (round(pacman_position[0]),round(pacman_position[1])) == (round(self.ghost_position[0]),round(self.ghost_position[1])): #if ghost and pacman intersect
		
			return True




#Initializing pygame
# pygame.init()
screen = pygame.display.set_mode((672,640), 0, 32)
# background = pygame.surface.Surface((672,640)).convert()
background=wallbackground
path=black

#Initializing variables
layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
pacman_position = (10,13)
ghost_position = (10,10)
ghost_direction = TOP
blinky_position = (10,10)
blinky_direction = TOP
# background.fill((0,0,0))
move_direction=RIGHT
upDir=True
downDir=False
leftDir=False
rightDir=False
# Main game loop 

for col in range(cols):
		for row in range(rows):
			value = layout[row][col]
			pos = (col, row)

eyeDir = 0

blinkyGhost=ghost(blinky,ghost_position,ghost_direction,eyeDir)
inkyGhost=ghost(inky,ghost_position,ghost_direction,eyeDir)
pinkyGhost=ghost(pinky,ghost_position,ghost_direction,eyeDir)
clydeGhost=ghost(clyde,ghost_position,ghost_direction,eyeDir)

pacmanTitle = myfontTitle.render('PAC-MAN',False,(255,255,0))
classic = myfont1.render('1) CLASSIC',False,(255,255,255))
ghostMode = myfont1.render('2) GHOST MODE',False,(255,255,255))
twoPlayer = myfont1.render('3) 2 PLAYER',False,(255,255,255))
pressPToPlay = myfont1.render('PRESS P TO PLAY',False,(255,255,255))
pressQToQuit = myfont1.render('PRESS Q TO QUIT',False,(255,255,255))
copyrightRhythm = myfont.render('© Rhythm Patel 2018',False,(255,255,255))

menu = True

while True:

	while menu:

		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		# screen.blit(menuImg,(0,0))
		screen.blit(pacmanTitle,(130,40))
		# screen.blit(classic,(190,250))
		# screen.blit(ghostMode,(190,310))
		# screen.blit(twoPlayer,(190,370))
		screen.blit(pressPToPlay,(150,400))
		screen.blit(pressQToQuit,(150,480))
		screen.blit(copyrightRhythm,(140,580))
		pygame.display.update()
		
		keys1=pygame.key.get_pressed() #created a dict with keys in buttons of keyboard

		if keys1[K_p]:
			mode = 1
			menu = False
			startTime = time.time()

		if keys1[K_q]:
			exit()

	# clock.tick(9)
	# screen.blit.background
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()


	elapsedTime=time.time()-startTime
	gameTime=time.time()-startTime

	text = myfont.render('{} {}       {} {}'.format('SCORE :',str(score),'TIME :',str(round(gameTime,2))), False, (255,255,255))
	# text = myfont.render('SCORE : '+str(score)+'       TIME : '+str(round(elapsedTime,2)), False, (255,255,255))
	youDied = myfont.render('{}'.format('YOU DIED!'),False,(255,255,255))
	gameOver = myfont.render('{}'.format('GAME OVER'),False,(173,255,47))
	youWon = myfont.render('{}'.format('YOU WON'),False,(173,255,47))
	livesLeft = myfont.render('{} {}'.format('LIVES:',str(lives)),False,(255,255,255))

	keys=pygame.key.get_pressed() #created a dict with keys in buttons of keyboard
	
	if keys[K_q]:
		exit()
		
	if keys[K_LEFT] or move_direction==LEFT: #if left key pressed or current direction left
		pacman_position=(pacman_position[0],round(pacman_position[1])) #align to walls
		value=layout[int(pacman_position[1])][int(pacman_position[0])] #extracts the next position
		if value!='w':
			move_direction=LEFT #goes left if not wall
			leftDir=True
			rightDir=False
			upDir=False
			downDir=False
		else:
			move_direction=(0,0) #wont move as hitting wall

	if keys[K_RIGHT] or move_direction==RIGHT: #if right key pressed or current direction right
		pacman_position=(pacman_position[0],round(pacman_position[1])) #align to walls
		value=layout[int(pacman_position[1])][int(pacman_position[0])+1] #extracts the next position
		if value!='w':
			move_direction=RIGHT #goes right if not wall
			rightDir=True
			leftDir=False
			upDir=False
			downDir=False
		else:
			move_direction=(0,0) #wont move as hitting wall

	if keys[K_UP] or move_direction==TOP: #if up key pressed or current direction up
		pacman_position=(round(pacman_position[0]),pacman_position[1]) #align to walls
		value=layout[int(pacman_position[1])][int(pacman_position[0])] #extracts the next position
		if value!='w':
			move_direction=TOP #goes up if not wall
			upDir=True
			downDir=False
			rightDir=False
			leftDir=False
		else:
			move_direction=(0,0) #wont move as hitting wall

	if keys[K_DOWN] or move_direction==DOWN: #if down key pressed or current direction down
		pacman_position=(round(pacman_position[0]),pacman_position[1]) #align to walls
		value=layout[int(pacman_position[1])+1][int(pacman_position[0])] #extracts the next position
		if value!='w':
			move_direction=DOWN #goes down if not wall
			downDir=True
			upDir=False
			leftDir=False
			rightDir=False
		else:
			move_direction=(0,0) #wont move as hitting wall


	if (round(pacman_position[0]),round(pacman_position[1]))==(-1,9) and move_direction==LEFT:
		pacman_position=(21,9) #For left portal

	if (round(pacman_position[0]),round(pacman_position[1]))==(21,9) and move_direction==RIGHT:
		pacman_position=(-1,9) #For right portal


	if (round(pacman_position[0]),round(pacman_position[1]))==(10,7) and move_direction==DOWN:
		move_direction=(0,0) #So Pacman can't enter ghost den
		

	if layout[round(pacman_position[1])][round(pacman_position[0])]=='c':
		score+=10
		layout[round(pacman_position[1])][round(pacman_position[0])]='.' #changes coin to empty path


	screen.blit(background, (0,0))

	#Draw board from the 2d layout array.
	#In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins
	
	noOfCoinsFlag=1
	for col in range(cols):
		for row in range(rows):
			value = layout[row][col]
			pos = (col, row)
			if value == 'w':
				draw_wall(screen, pos)
			elif value == 'c':
				noOfCoinsFlag=0
				pixels=pixels_from_points(pos)
				pygame.draw.rect(screen, (0,0,0), [pixels, (WIDTH, HEIGHT)])
				draw_coin(screen, pos)
			else:
				pixels=pixels_from_points(pos)
				#  pygame.draw.rect(screen, (0,0,0), [pixels, (WIDTH, HEIGHT)])
				screen.blit(path,pixels)

	if noOfCoinsFlag==1:
		screen.blit(youWon,(266,160))


	screen.blit(text,(28,6))
	screen.blit(livesLeft,(460,614))

	#Draw the player
	draw_pacman(screen, pacman_position)

	
	if elapsedTime < 2:
		blinkyGhost.reset()
	else:
		blinkyGhost.random()

	blinkyGhost.draw_ghost()
	# blinkyGhost.intersect()


	if elapsedTime < 6:
		inkyGhost.reset()
	else:
		inkyGhost.random()

	inkyGhost.draw_ghost()
	# inkyGhost.intersect()

	if elapsedTime < 10:
		pinkyGhost.reset()
	else:
		pinkyGhost.random()

	pinkyGhost.draw_ghost()
	# pinkyGhost.intersect()

	if elapsedTime < 16:
		clydeGhost.reset()
	else:
		clydeGhost.random()

	clydeGhost.draw_ghost()
	# clydeGhost.intersect()

	if blinkyGhost.intersect() or inkyGhost.intersect() or pinkyGhost.intersect() or clydeGhost.intersect():
		lives-=1
		pacman_position=(10,13)
		move_direction=TOP
		blinkyGhost.reset()
		inkyGhost.reset()
		pinkyGhost.reset()
		clydeGhost.reset()
		elapsedTime=0
		
	# draw_ghost(screen,ghost_position,blinky[eyeDir])

	#Update player position based on movement.
	pacman_position = add_to_pos(pacman_position, (move_direction[0]*0.1,move_direction[1]*0.1))
	blinkyGhost.ghost_position = add_to_pos(blinkyGhost.ghost_position, (blinkyGhost.ghost_direction[0]*0.1,blinkyGhost.ghost_direction[1]*0.1))
	inkyGhost.ghost_position = add_to_pos(inkyGhost.ghost_position, (inkyGhost.ghost_direction[0]*0.1,inkyGhost.ghost_direction[1]*0.1))
	pinkyGhost.ghost_position = add_to_pos(pinkyGhost.ghost_position, (pinkyGhost.ghost_direction[0]*0.1,pinkyGhost.ghost_direction[1]*0.1))
	clydeGhost.ghost_position = add_to_pos(clydeGhost.ghost_position, (clydeGhost.ghost_direction[0]*0.1,clydeGhost.ghost_direction[1]*0.1))


	#Update the display
	# fpsClock.tick(FPS)
	pygame.display.update()

	if lives==0:
		deathTime=time.time()

		if time.time()-deathTime<=3:
			translucentLayer(screen, pos)
			screen.blit(gameOver,(246,160)) #display Game Over message
			pygame.display.update()
			score = 0
			menu = True
			lives = 3
			pacman_position = (10,13)
			move_direction = RIGHT
			blinkyGhost.reset()
			inkyGhost.reset()
			pinkyGhost.reset()
			clydeGhost.reset()


	#Wait for a while, computers are very fast.
	time.sleep(0.004)