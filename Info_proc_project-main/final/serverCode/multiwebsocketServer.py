import pygame
import pygame, sys
from pygame.locals import *
import random
import asyncio
import websockets


BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,180,0)
BLUE = (50,200,255)
FILL = BLACK
TEXT = WHITE

pygame.init()

#Here you can specify the structure of the neural network. This includes the input layer and output layer.
#e.g 3 inputs, 5 node hidden layer, 4 outputs would be [3, 5, 4]
#Be sure to update this if you add inputs

size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pong")


class Paddle:
	
	def __init__(self, x = size[0]/2, xspeed = 0, coefs = 0, intercepts = 0):
		self.x = x
		self.xlast = x-xspeed
		self.xspeed = xspeed
		self.alive = True
		self.score = 0
		self.command = 2
		self.playerLeft = True
	 

	#Reset score, speed and position
	def reset(self):
		self.x = size[1]/2
		self.xlast = size[1]/2
		self.xspeed = 0
		self.alive = True
		self.score = 0
	
	#Update position based on speed		
	def update(self):
		#self.xlast = self.x
		self.x += self.speed
		if self.x < 0:
			self.x = 0
		elif self.x > size[0]-100:
			self.x=size[0]-100
		
		self.ylast = self.y
	
	#Draw the paddle to the screen	   
	'''def draw(self):
		pygame.draw.rect(screen, BLACK, [0, self.y, 20, 100])  # Outer rectangle
		pygame.draw.rect(screen, RED, [2, self.y+2, 20-4, 100-4])  # Inner rectangle'''

class Ball:
	
	def __init__(self, x = size[0]/2, y = size[1]/2, xspeed = -random.randrange(3,6), yspeed = random.randrange(3,6)):
		self.x = x
		self.y = y
		self.xlast = x-xspeed
		self.ylast = y-yspeed
		self.xspeed = xspeed
		self.yspeed = yspeed
		self.alive = True
	
	#Update position based on speed 
	def update(self, paddle1, paddle2):
		self.xlast = self.x
		self.ylast = self.y
		
		self.x += self.xspeed
		self.y += self.yspeed

		#Accounts for bouncing off walls and paddle
		if self.y>size[1]-35:
			self.y=size[1]-35
			self.yspeed = self.yspeed * -1
			print("bounce bottom")
		elif self.y < 20 and self.x >= paddle1.x and self.x <= paddle1.x + 100:
			self.y = 20
			self.yspeed =-1*(self.yspeed+0.2)
			paddle1.score += 1
			print("bounce paddle 1")

		elif self.y > size[1]-20 and self.x >= paddle2.x and self.x <= paddle2.x + 100:
			self.y = 20
			self.yspeed =-1*(self.yspeed+0.2)
			paddle1.score += 1
			print("bounce paddle 2")

		elif self.y<0 or self.y>size[1]-15:
			self.yspeed = self.yspeed * -1
			paddle1.alive = False
			paddle2.alive = False
			
			print("dead")
			
	#Draw ball to screen	   
	'''def draw(self):
		pygame.draw.rect(screen,WHITE,[self.x,self.y,15,15])'''

#keydown and keyup for host to control paddle as well    
'''def keydown(event, paddle):    
    if (event.key == K_UP) or (event.key == K_w):
        paddle.yspeed = -8
    elif (event.key == K_DOWN) or (event.key == K_s):
        paddle.yspeed = 8

def keyup(event, paddle):    
    if event.key in (K_w, K_s,K_UP, K_DOWN):
        paddle.yspeed = 0'''

def keyEvent(key, paddle1, paddle2):
	if (key == "1'b'w'"):
		paddle1.xspeed = -8
	elif (key == "1'b's'"):
		paddle1.xspeed = 8
	elif (key == "2'b'w'"):
		paddle2.xspeed = -8
	elif (key == "2'b's'"):
		paddle2.xspeed = 8
	else:
		paddle1.xspeed = 0
		paddle2.xspeed = 0

done = False
score = 0
command = "stop"
clock=pygame.time.Clock()

COUNT = 100

#create sprites

async def play(websocket, path):
	print("HERE")
	while True: 
		try:
			myPaddle1.update()
			myPaddle2.update()
			myBall.update()
			print("SUB")
			await websocket.send(myPaddle1, myPaddle2, myBall)
		except websocket.exceptions.ConnectionClosed:
			print("Connection Closed")
			break
		
async def echo(websocket, path):
    #asyncio.create_task(play(websocket))
	async for message in websocket:
		print(f"Received message: {message}")
		keyEvent(message, myPaddle1, myPaddle2)
		myPaddle1.update()
		myPaddle2.update()
		myBall.update(myPaddle1, myPaddle2)
		info = [myPaddle1.y, myPaddle2.y, myBall.x, myBall.y]
		await websocket.send(str(info))

myPaddle1 = Paddle()
myPaddle2 = Paddle()
myBall = Ball()

start_server = websockets.serve(echo, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


