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
	
	def __init__(self, y = size[1]/2, yspeed = 0, coefs = 0, intercepts = 0):
		self.y = y
		self.ylast = y-yspeed
		self.yspeed = yspeed
		self.alive = True
		self.score = 0
		self.command = 2
		self.playerLeft = True
	 

	#Reset score, speed and position
	def reset(self):
		self.y = size[1]/2
		self.ylast = size[1]/2
		self.yspeed = 0
		self.alive = True
		self.score = 0
	
	#Update position based on speed		
	def update(self):
		#self.xlast = self.x
		self.y += self.yspeed
		if self.y < 0:
			self.y = 0
		elif self.y > size[1]-100:
			self.y=size[1]-100
		
		self.ylast = self.y
	
	#Draw the paddle to the screen	   
	def draw(self):
		pygame.draw.rect(screen, BLACK, [0, self.y, 20, 100])  # Outer rectangle
		pygame.draw.rect(screen, RED, [2, self.y+2, 20-4, 100-4])  # Inner rectangle



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
	def update(self, paddle):
		self.xlast = self.x
		self.ylast = self.y
		
		self.x += self.xspeed
		self.y += self.yspeed

		#Accounts for bouncing off walls and paddle
		if self.x>size[0]-15:
			self.x=size[0]-15
			self.xspeed = self.xspeed * -1
			print("bounce right")
		elif self.y>size[1]-35:
			self.y=size[1]-35
			self.yspeed = self.yspeed * -1
			print("bounce bottom")
		elif self.y<0:
			self.y=0
			self.yspeed = self.yspeed * -1
			print("bounce top")
		elif self.x < 20 and self.y >= paddle.y and self.y <= paddle.y + 100:
			self.x = 20
			self.xspeed =-1*(self.xspeed+0.2)
			paddle.score += 1
			print("bounce paddle")
		elif self.x<0:
			self.xspeed = self.xspeed * -1
			paddle.alive = False
			paddle.score -= round(abs((paddle.y+50)-self.x)/100,2)
			print("dead")
			
	#Draw ball to screen	   
	def draw(self):
		pygame.draw.rect(screen,WHITE,[self.x,self.y,15,15])

    
def keydown(event, paddle):    
    if (event.key == K_UP) or (event.key == K_w):
        paddle.yspeed = -8
    elif (event.key == K_DOWN) or (event.key == K_s):
        paddle.yspeed = 8

def keyup(event, paddle):    
    if event.key in (K_w, K_s,K_UP, K_DOWN):
        paddle.yspeed = 0

def keyEvent(key, paddle):
	if (key == "b'w'") or (key == K_w):
		paddle.yspeed = -8
	elif (key == "b's'") or (key == K_s):
		paddle.yspeed = 8
	else:
		paddle.yspeed = 0

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
			myPaddle.update()
			myBall.update()
			print("SUB")
			await websocket.send(myPaddle, myBall)
		except websocket.exceptions.ConnectionClosed:
			print("Connection Closed")
			break
		
async def echo(websocket, path):
    #asyncio.create_task(play(websocket))
	async for message in websocket:
		print(f"Received message: {message}")
		keyEvent(message, myPaddle)
		myPaddle.update()
		myBall.update(myPaddle)
		info = [myPaddle.y, myBall.x, myBall.y]
		await websocket.send(str(info))

myPaddle = Paddle()
myBall = Ball()

start_server = websockets.serve(echo, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


