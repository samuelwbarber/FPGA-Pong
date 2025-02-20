import asyncio
import websockets
#import msvcrt
import pygame
import pygame, sys
from pygame.locals import *
import ast

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,180,0)
BLUE = (50,200,255)
FILL = BLACK
TEXT = WHITE

CLIENT = 1

size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pong")
clock=pygame.time.Clock()

pygame.init()

def draw(paddle1_y, paddle2_y, ball_x, ball_y):
    screen.fill(FILL)
    pygame.draw.rect(screen, BLACK, [0, paddle1_y, 20, 100])  # Outer rectangle
    pygame.draw.rect(screen, RED, [2, paddle1_y+2, 20-4, 100-4])  # Inner rectangle

    pygame.draw.rect(screen, BLACK, [size[0], paddle2_y, 20, 100])  # Outer rectangle
    pygame.draw.rect(screen, RED, [size[0]-2, paddle2_y+2, 20-4, 100-4])  # Inner rectangle

    pygame.draw.rect(screen,WHITE,[ball_x,ball_y,15,15])
    pygame.display.flip()
    clock.tick(60)


def decode(message):
    parameters = ast.literal_eval(message)
    draw(parameters[0], parameters[1], parameters[2], parameters[3])
    print(f"Received from server: {message}")

done = False

async def player1():
    uri = "ws://ec2-18-130-198-236.eu-west-2.compute.amazonaws.com:6789"
    message = 0
    async with websockets.connect(uri) as websocket:
        while not done:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if (event.key == K_UP):
                        message = "1'b'w'"
                    elif (event.key == K_DOWN):
                        message = "1'b's'"
                    elif (event.key == K_q):
                        message = "stop"
                elif event.type == KEYUP:
                    message = 0
                await websocket.send(str(message))
                response = await websocket.recv()
                decode(response)
            
            await websocket.send(str(message))
            response = await websocket.recv()
            decode(response)

asyncio.get_event_loop().run_until_complete(player1())

pygame.quit()
