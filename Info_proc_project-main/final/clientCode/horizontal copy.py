import asyncio
import websockets
#import msvcrt
import pygame
import pygame, sys
from pygame.locals import *
import ast

import sys
import os
pygame.init()
pygame.font.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,180,0)
BLUE = (50,200,255)
WATERMELON = (252,108,133)
PEACH =  (255,218,185)
GREEN = (172,225,175)

FILL = PEACH
TEXT = BLACK

CLIENT = 1

size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pong")
clock=pygame.time.Clock()

font = pygame.font.Font(None, 36)

pygame.init()

def draw(paddle1_x, paddle2_x, ball_x, ball_y, paddle1_score, paddle2_score):
    screen.fill(FILL)

    if (paddle1_score + paddle2_score == 3):
        screen.fill(WATERMELON)
        gameover = font.render(f'GAME OVER', True, TEXT)
        screen.blit(gameover, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3)
        clock.tick(60)
    
    else:
        #score
        score_text1 = font.render(f'Score: {paddle1_score}', True, TEXT)
        score_text2 = font.render(f'Score: {paddle2_score}', True, TEXT)
        screen.blit(score_text1, (500, 500))
        screen.blit(score_text2, (100, 100))


        #Player on Bottom
        pygame.draw.rect(screen, GREEN, [paddle1_x, size[1], 100, 20])  # Outer rectangle
        pygame.draw.rect(screen, GREEN, [paddle1_x+2, size[1]-20, 100-4, 20-4])  # Inner rectangle
        ##Player on Top
        pygame.draw.rect(screen, GREEN, [paddle2_x, 0, 100, 20])  # Outer rectangle
        pygame.draw.rect(screen, GREEN, [paddle2_x+2,2, 100-4, 20-4])  # Inner rectangle

        pygame.draw.rect(screen,WATERMELON,[ball_x,ball_y,15,15])
        pygame.display.flip()
        clock.tick(60)

def welcome(input, opponent):
    screen.fill(GREEN)

    if (input == 0):
        welcome = font.render('Welcome! Waiting for opponent', True, TEXT)
    
    elif (input == 1):
        welcome = font.render(f'{opponent} is ready to play!', True, TEXT)
    screen.blit(welcome, (500, 500))
    pygame.display.flip()

    clock.tick(60)
    



def decode(message):
    parameters = ast.literal_eval(message)
    if len(parameters == 3):
        welcome( message[1], message[2])
        print(f"Received from server: {message}")
        return [message[0], message[1]] #client + status
    
    elif len(parameters == 6):
        draw(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5])
        print(f"Received from server: {message}")
        return [0,0]    #dont need it
    



async def play(CLIENT):
    uri = "ws://ec2-18-134-74-68.eu-west-2.compute.amazonaws.com:6789"
    message = 0
    
    async with websockets.connect(uri) as websocket:

        for event in pygame.event.get():
           
            if event.type == QUIT:
                await websocket.send("STOP:" + CLIENT)
                print("QUIT")
                pygame.quit()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT):
                    message = CLIENT + "'b'w'"
                elif (event.key == K_RIGHT):
                    message = CLIENT + "'b's'"
            elif event.type == KEYUP:
                message = 0
            await websocket.send(str(message))

            response = await websocket.recv()
            status = decode(response)
            await  asyncio.sleep(3)
                


async def welcome():
    uri = "ws://ec2-18-134-74-68.eu-west-2.compute.amazonaws.com:6789"
    message = 0
    
    async with websockets.connect(uri) as websocket:
        user = input("Enter User: ")

        for event in pygame.event.get():
            if event.type == K_RETURN:
                    message = ("ENTER:" + user)
            elif event.type == QUIT:
                    message = ("STOP:" + user) 
                    pygame.quit()
            else:
                message = 0
            await websocket.send(str(message))

            response = await websocket.recv()
            status = decode(response)    #should be 2 arguments 
            print("waiting " + response)
            await  asyncio.sleep(3)
            return status

            
async def main():
    while True:
        result = await welcome()
        if ((result == [1,1]) or (result == [2,1])) : #if the other client has pressed enter
            await play(result[0])
            break

loop = asyncio.get_event_loop()
# Run until complete
loop.run_until_complete(main())

#asyncio.get_event_loop().run_until_complete(play())
pygame.quit()
