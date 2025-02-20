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
	 

	#Reset speed and position
	def reset(self):
		self.x = size[0]/2
		self.xlast = size[0]/2
		self.xspeed = 0
		self.alive = True
	
	#Update position based on speed		
	def update(self):
		#self.xlast = self.x
		self.x += self.xspeed
		if self.x < 0:
			self.x = 0
		elif self.x > size[0]-100:
			self.x=size[0]-100
		
		self.xlast = self.x
	
	#Draw the paddle to the screen	   
	'''def draw(self):
		pygame.draw.rect(screen, BLACK, [0, self.y, 20, 100])  # Outer rectangle
		pygame.draw.rect(screen, RED, [2, self.y+2, 20-4, 100-4])  # Inner rectangle'''

class Ball:
	
	def __init__(self, x = size[0]/2, y = size[1]/2, xspeed = -random.randrange(1,5), yspeed = random.randrange(1,5)):
		self.x = x
		self.y = y
		self.xlast = x-xspeed
		self.ylast = y-yspeed
		self.xspeed = xspeed
		self.yspeed = yspeed
	
	def reset(self, x = size[0]/2, y = size[1]/2):
		self.x = x
		self.y = y
		self.xlast = x-self.xspeed
		self.ylast = y-self.yspeed
		self.xspeed = random.choice([-1, 1]) * 2.5
		self.yspeed = random.choice([-1, 1]) * 2.5
	
	#Update position based on speed 
	def update(self, paddle1, paddle2):
		self.xlast = self.x
		self.ylast = self.y
		
		self.x += self.xspeed
		self.y += self.yspeed

		#Accounts for bouncing off walls and paddle
		if self.x>size[0]-15:
			self.x=size[0]-15
			self.xspeed = self.xspeed * -1
			print("bounce right")
		elif self.x<0:
			self.x=0
			self.xspeed = self.xspeed * -1
			print("bounce left")

		#paddle 1 is on the bottom, paddle 2 is on the top
		elif self.y < 20 and self.x >= paddle2.x and self.x <= paddle2.x + 100:
			self.y = 20
			self.yspeed =-1*(self.yspeed+0.1)
			print("bounce paddle 2")

		elif self.y > size[1]-35 and self.x >= paddle1.x and self.x <= paddle1.x + 100:
			self.y = size[1]-35
			self.yspeed =-1*(self.yspeed+0.1)
			print("bounce paddle 1")

		elif self.y<0:
			self.y = 0
			self.yspeed = self.yspeed * -1	
			print("paddle 2 dead")
			paddle1.score += 1
			self.reset()


		elif self.y>size[1]:
			self.y = size[1]
			self.yspeed = self.yspeed * -1	
			print("paddle 1 dead")
			paddle2.score += 1
			self.reset()
			
			

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

# async def play(websocket, path):
# 	print("HERE")
# 	while True: 
# 		try:
# 			myPaddle1.update()
# 			myPaddle2.update()
# 			myBall.update()
# 			print("SUB")
# 			await websocket.send(myPaddle1, myPaddle2, myBall)
# 		except websocket.exceptions.ConnectionClosed:
# 			print("Connection Closed")
# 			break
		
async def echo(websocket, path):
	async for message in websocket:
		print(f"Received message: {message}")
		if message.startswith("STOP: "):  # Check if stop message is received
			client_stop = message[5:]
			print(client_stop + "STOP")
			clients.pop(int(client_stop)-1)
		if message.startswith("USER:"):
			user = message[6:]
			if user in clients:
				await websocket.send(str(clients.index(user)+1))
			if len(clients)>2:
				await websocket.send("Already 2 players")
			else:
				clients.append(user)
				await websocket.send(str(clients.index(user)+1))
		if len(clients)==2: 
			keyEvent(message, myPaddle1, myPaddle2)
			myPaddle1.update()
			myPaddle2.update()
			myBall.update(myPaddle1, myPaddle2)
			info = [myPaddle1.x, myPaddle2.x, myBall.x, myBall.y, myPaddle1.score, myPaddle2.score]
			await websocket.send(str(info))  # Send game state to client
		else: 
			await websocket.send("Waiting Player 2")

clients = []
myPaddle1 = Paddle()
myPaddle2 = Paddle()
myBall = Ball()

start_server = websockets.serve(echo, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


