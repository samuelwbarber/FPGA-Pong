import asyncio
import websockets
#import msvcrt
import pygame
import pygame, sys
from pygame.locals import *
import ast
import sys
import os
import intel_jtag_uart
import time
pygame.init()
pygame.font.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,69,0)
GREEN = (0,180,0)
BLUE = (50,200,255)
WATERMELON = (252,108,133)
PEACH =  (255,218,185)
GREEN = (172,225,175)
NICE_BLUE = (0,0,205)
FILL = PEACH
TEXT = BLACK

size = (800,600)




screen = pygame.display.set_mode(size)
pygame.display.set_caption("pong")
clock=pygame.time.Clock()
font = pygame.font.Font(None, 36)


pygame.init()

def countdown_1():
    background = pygame.image.load('copy1.jpeg').convert()
    background = pygame.transform.smoothscale(background, size)
    screen.blit(background,(0,0))
    ju = initialise_jtag()
    print("Countdown")
    one = font.render(f'3', True, TEXT)
    screen.blit(one, (400, 300))
    ju.write(b'a')
    pygame.display.flip()
    pygame.time.wait(1000)

    background = pygame.image.load('copy2.jpeg').convert()
    background = pygame.transform.smoothscale(background, size)
    screen.blit(background,(0,0))
    two = font.render(f'2', True, TEXT)
    screen.blit(two, (400, 300))
    ju.write(b'b')
    pygame.display.flip()
    pygame.time.wait(1000)

    background = pygame.image.load('copy3.jpeg').convert()
    background = pygame.transform.smoothscale(background, size)
    screen.blit(background,(0,0))
    three = font.render(f'1', True, TEXT)
    screen.blit(three, (400, 300))
    ju.write(b'c')
    pygame.display.flip()
    pygame.time.wait(1000)

    ju.write(b'd')

    clock.tick(60)
    print("Countdown END")
    ju.close()

def display_screen_with_options(name):
    background1 = pygame.image.load('background3.jpg').convert()
    background1 = pygame.transform.smoothscale(background1, size)
    # Texts
    screen.blit(background1,(0,0))
    one_text = font.render('1', True, BLACK)
    two_text = font.render('2', True, BLACK)
    welcome_text = font.render(f"Welcome {name}", True, WHITE)
    replay_text = font.render('Replays', True, WHITE)
    multiplayer_text = font.render('Multiplayer', True, WHITE)
    pygame.display.flip()

    # Main loop
    running = True
    while running:

        # Adjusted button positions for more separation
        button1_pos = (size[0] / 2 - 200,  size[1] / 2)
        button2_pos = (size[0] / 2 + 100, size[1] / 2)

        # Welcome text position
        welcome_text_rect = welcome_text.get_rect(center=(size[0] / 2, size[1] / 2 - 100))
        screen.blit(welcome_text, welcome_text_rect)

        # Button creation and placement
        button1 = pygame.Surface((100, 50))
        button1.fill(WATERMELON)
        button2 = pygame.Surface((100, 50))
        button2.fill(WATERMELON)

        screen.blit(button1, button1_pos)
        screen.blit(button2, button2_pos)
        
        # Button labels
        screen.blit(one_text, (button1_pos[0] + 35, button1_pos[1] + 10))
        screen.blit(two_text, (button2_pos[0] + 35, button2_pos[1] + 10))
        
        # Descriptive texts below buttons
        screen.blit(replay_text, (button1_pos[0] + 10, button1_pos[1] + 60))
        screen.blit(multiplayer_text, (button2_pos[0] - 30, button2_pos[1] + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # Button click detection
                if button1.get_rect(topleft=button1_pos).collidepoint(pos):
                    return 1
                elif button2.get_rect(topleft=button2_pos).collidepoint(pos):
                    return 2

        pygame.display.flip()

def ask_text(screen_message):
    # Set up font
    font_size = 32
    print("got here")
    font = pygame.font.Font(None, font_size)

    # Email input string
    email_input = ''

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    email_input = email_input[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Email entered:", email_input)
                    return email_input
                else:
                    email_input += event.unicode
        
        background = pygame.image.load('background6.jpg').convert()
        background = pygame.transform.smoothscale(background, size)
        screen.blit(background,(0,0))
        
        # Render prompt and input text to get their rects for positioning
        prompt_surface = font.render(screen_message, True, WHITE)
        input_surface = font.render(email_input, True, WHITE)
        prompt_rect = prompt_surface.get_rect(center=(size[0] / 2, size[1] / 2 - 20))
        input_rect = input_surface.get_rect(center=(size[0] / 2, size[1]/ 2 + 20))
        
        # Blit the surfaces on the screen at their new positions
        screen.blit(prompt_surface, prompt_rect)
        screen.blit(input_surface, input_rect)
        
        # Update display
        pygame.display.flip()

def welcome(name):
    background2 = pygame.image.load('background3.jpg').convert()
    background2 = pygame.transform.smoothscale(background2, size)
    screen.blit(background2,(0,0))
    message = font.render(f'Welcome {name}', True, WHITE)
    screen.blit(message, (200, 300))
    pygame.display.flip()
    pygame.time.wait(2)
    
    screen.blit(message, (100, 300))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if button1.get_rect().collidepoint(pos):
                return 1
            elif button2.get_rect().collidepoint(pos):
                return 2

    clock.tick(60)

def waiting():
    background3 = pygame.image.load('background1.jpg').convert()
    background3 = pygame.transform.smoothscale(background3, size)
    screen.blit(background3,(0,0))
    message = font.render(f'Waiting for other player...', True, (255, 255, 255))
    screen.blit(message, (200, 200))
    pygame.display.flip()
    pygame.time.wait(1)
    clock.tick(60)

def gameover_draw(winner):
    font2 = pygame.font.Font(None, 70)
    background4 = pygame.image.load('background4.jpg').convert()
    background4 = pygame.transform.smoothscale(background4, size)
    screen.blit(background4,(0,0))
    gameover = font2.render(f'{winner} WON', True, WHITE)
    screen.blit(gameover, (300, 500))
    pygame.display.flip()
    pygame.time.wait(3000)
    clock.tick(60)

def draw(paddle1_x, paddle2_x, ball_x, ball_y, paddle1_score, paddle2_score, client = "1"):
    background = pygame.image.load('background2.jpg').convert()
    background = pygame.transform.smoothscale(background, size)
    screen.blit(background,(0,0))
    #score
    score_text1 = font.render(f'Score: {paddle1_score}', True, WHITE)
    score_text2 = font.render(f'Score: {paddle2_score}', True, WHITE)
    screen.blit(score_text1, (500, 450))
    screen.blit(score_text2, (100, 100))

    #Player on Bottom
    if client == "1": 
        PLAYER1_COLOR = RED
        PLAYER2_COLOR = NICE_BLUE
    elif client =="2":
        PLAYER2_COLOR = RED
        PLAYER1_COLOR = NICE_BLUE
    
    pygame.draw.rect(screen, PLAYER1_COLOR, [paddle1_x, size[1], 100, 20])  # Outer rectangle
    pygame.draw.rect(screen, PLAYER1_COLOR,  [paddle1_x+2, size[1]-20, 100-4, 20-4])  # Inner rectangle
    ##Player on Top
    pygame.draw.rect(screen, PLAYER2_COLOR, [paddle2_x, 0, 100, 20])  # Outer rectangle
    pygame.draw.rect(screen, PLAYER2_COLOR, [paddle2_x+2,2, 100-4, 20-4])  # Inner rectangle

    pygame.draw.rect(screen,WATERMELON,[ball_x,ball_y,15,15])
    pygame.display.flip()
    clock.tick(60)


def decode(message, PLAYER=0): 
    print("decode" + PLAYER)
    parameters = ast.literal_eval(message)
    draw(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], PLAYER)
    print(f"Received from server: {message}")
    
    if PLAYER == '1':
        print("score from decode" + str(parameters[4]))
        return parameters[4]
    else:
        print("score from decode" + str(parameters[5]))
        return parameters[5]

def initialise_jtag():
    try:
        ju = intel_jtag_uart.intel_jtag_uart()

    except Exception as e:
        print(e)
        sys.exit(0)

    return ju



CLIENT = 0
PLAYER = 0

async def play():
   uri = "ws://ec2-13-43-121-29.eu-west-2.compute.amazonaws.com:6789"
   message = 0
   print("here")
   async with websockets.connect(uri) as websocket:
        print("Connected to server")
        email = ask_text("Please enter your email: ")
        
        await websocket.send("0: " + email)    #sending email
        response = await websocket.recv()    #response is either NEW USER or NAME

        #case1: new client
        if  response.startswith("NEW"): 
            print("New user")
            name = ask_text("Please enter your usename: ")
            await websocket.send("1: " + name + "/" + email)
            response = await websocket.recv()
        CLIENT = response[0]
        print("CLIENT: ")
        print(CLIENT)
        
        #decode message
        print(response)
         #display welcome name 
        myName = response[2:]
        await websocket.send("5 VERF " + str(CLIENT))
        correct_code = False
        while not correct_code:
            code = ask_text("Please enter your 5-digit code: ")
            await websocket.send("5 " + str(CLIENT) + ": " + code)
            response = await websocket.recv()
            if response == "OK":
                correct_code = True
            else:
                print("Incorrect code, try again")

        
        #player decides which character either 1 or 2
        while True:
            character = display_screen_with_options(myName)
            print(CLIENT, character)
            await websocket.send("2 " + str(CLIENT) + " :" + str(character))
            response = await websocket.recv()
            print(response)
            #response will be WAITING or PLAY

            if response.startswith("REPLAY"): #1 selected
                replay = ast.literal_eval(response[7:])
                replay_index = 0
                while replay_index < len(replay):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    step = replay[replay_index]
                    draw(step[0], step[1], step[2], step[3], step[4], step[5])
                    replay_index += 1
                    clock.tick(60)
                print("replay end")
            elif response.startswith("NO REPLAY"):
                print("no replay")
            else: #2 selected
                PLAYER = response[4]
                while response.startswith("WAIT"):
                    print("waiting for other player")
                    waiting()
                    await websocket.send("4 " + str(CLIENT) + " :" + str(character)) #asking if still wait 
                    response = await websocket.recv()
                    print(response)
                countdown_1()
                #response will be PLAY - THROWS an ERROR ATM
                #CLIENT = await websocket.recv()              #get client  
                #print(f"CLIENT: {CLIENT}")
                if response.startswith("PLAY"):
                    message = "3 " + PLAYER + " 0"
                    print("here")

                    ju = initialise_jtag()
                    ju.write(b'0')
                    time.sleep(0.1)

                    while PLAYER != "0":
                        vals = (ju.read()).replace(bytes('\n', "utf-8"), bytes(' ', "utf-8"))
                        vals = (vals[-4:-2]).decode("utf-8")
                        ju.flush()
                        
                        message = "3 " + PLAYER + vals
                        await websocket.send(str(message))
                        response = await websocket.recv()

                        if response.startswith("WIN"):
                            if myName == response[4:]:
                                ju.write(b'w')
                            else:
                                ju.write(b'l')
                            ju.close()
                            gameover_draw(response[3:])
                            break
                        print(PLAYER)
                        score = decode(response, PLAYER)

                        #this is to send corresponding score to fpga
                        if CLIENT == '1':
                            ju.write(bytes(str(score), "utf-8"))
                        else:
                            ju.write(bytes(str(score), "utf-8"))

                        for event in pygame.event.get():
                            if event.type == QUIT:
                                await websocket.send("STOP: " + CLIENT)
                                print("QUIT")
                                pygame.quit() 


asyncio.get_event_loop().run_until_complete(play())
pygame.quit()
