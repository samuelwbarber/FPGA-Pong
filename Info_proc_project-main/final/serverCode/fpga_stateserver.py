import pygame
import pygame, sys
from pygame.locals import *
import random
import asyncio
import websockets
import psycopg2 
from smtplib import SMTP_SSL, SMTP_SSL_PORT
import emailcode


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

try:
    # Connect to your PostgreSQL database
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    print("PostgreSQL connection is open")
    
    # example usage
    #leaderboard = get_leaderboard()
   # print("Leaderboard:")
    #for row in leaderboard:
     ##   print(f"{row[0]} - Score: {row[1]}")

    # Close the cursor and connection
    #cursor.close()
    #connection.close()
    #print("PostgreSQL connection is closed")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

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
    
    def __init__(self, x = size[0]/2, y = size[1]/2, xspeed = -random.randrange(4,7), yspeed = random.randrange(4,7)):
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
        self.xspeed = random.choice([-1, 1]) * 2
        self.yspeed = random.choice([-1, 1]) * 2
    
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
            self.yspeed =-1*(self.yspeed+0.7)
            print("bounce paddle 2")

        elif self.y > size[1]-35 and self.x >= paddle1.x and self.x <= paddle1.x + 100:
            self.y = size[1]-35
            self.yspeed =-1*(self.yspeed+0.7)
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

done = False
score = 0
command = "stop"
clock=pygame.time.Clock()
clients = []
codes = {}
playing_clients = []
myPaddle1 = Paddle()
myPaddle2 = Paddle()
myBall = Ball()

def check_player(Email):
    sql= "SELECT COUNT(*) FROM USER_TBL WHERE Email = '"+Email+"';"
    data = (Email)
    cursor.execute(sql)
    player = cursor.fetchone()
    print(player)
    if player[0] != 0:
        return 1
    else:
        return 0

# if player exits, retrieve player info from USER_TBL table
def retrieve_player(Email):
    sql = "SELECT * FROM USER_TBL WHERE Email = '"+Email+"';"
    cursor.execute(sql)
    player = cursor.fetchall()
    return player

# if player does not exist, insert player info to USER_TBL table
def insert_player(Email, firstName, ColourR, ColourG, ColourB, IndexIcon):
    sql = "INSERT INTO USER_TBL (Email, firstName, ColourR, ColourG, ColourB, IndexIcon) VALUES ('"+Email+"','"+firstName+"',0,0,0,0);"
    cursor.execute(sql)
    connection.commit()

# update player score in USER_TBL table (check whether player wins or lose before updating?)
def update_score(ScoreInc, Email):
    sql = "UPDATE USER_TBL SET Score = Score + "+ScoreInc+" WHERE Email = '"+Email+"';"
    cursor.execute(sql)
    connection.commit()

def save_game(array, email):
    for index, element in enumerate(array):
        sql = "INSERT INTO GAME_TBL (Email, IndexVal, PosBallX, PosBallY, PosPaddle0, PosPaddle1) VALUES (email, index, )"
# data retrieval to output leaderboard
def get_leaderboard():
    sql = "SELECT firstName, Score FROM USER_TBL ORDER BY Score DESC LIMIT 10"
    print("Executing query:", sql)
    cursor.execute(sql)
    leaderboard = cursor.fetchall()
    return leaderboard

def saveGame(dat1a):
    data = [
    ['email1@example.com', 1, 10, 20, 30, 40],
    ['email2@example.com', 2, 15, 25, 35, 45]
    ]
    for row in data:
        cursor.execute("""
            INSERT INTO GAME_TBL (Email, IndexVal, PosBallX, PosBallY, PosPaddle0, PosPaddle1)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row[0], row[1], row[2], row[3], row[4], row[5])) +";"
    

def update_game(client, action):
    flag = True
    try:
        int(action)
    except ValueError:
        flag = False

    if (flag):
        accelerometer_val = -int(action)
        if client == "1": 
            myPaddle1.xspeed = accelerometer_val * 2
        if client == "2":
            myPaddle2.xspeed = accelerometer_val * 2

async def identify_user(mail, websocket):
    print("hello1")
    print(check_player(mail))
    if check_player(mail):
        print("hello")
        user = retrieve_player(mail)[0][1]
        print("hello")
        if mail in clients:
            await websocket.send("Client already in server!!")
        else: 
            print("hello")
            clients.append(mail)
            await websocket.send(str(clients.index(mail)+1) + " " + user)
            print("sent " + user)
            print("hello")
    else:
        await websocket.send("NEW")

async def new_user (message, websocket):
    index = message.find("/")
    mail = message[index+1:]
    user = message[3: index]
    insert_player(mail, user, 0, 0, 0, 0)
    clients.append(mail)
    print(clients.index(mail))
    await websocket.send(str(clients.index(mail)+1) + " " + user)
    print("sent " + str(clients.index(mail)+1) + " " + user)
    
async def multi_player_hub(client, websocket):
    player = clients[int(client)-1]
    print(playing_clients)
    if player in playing_clients:
        print("should not be here")
        if len(playing_clients) == 2:
            await websocket.send("PLAY")
        else:
            await websocket.send("WAIT" + str(len(playing_clients)))
    else: 
        print("here")
        if len(playing_clients) == 0:
            playing_clients.append(player)
            await websocket.send("WAIT" + str(len(playing_clients)))
            print("sent wait")
        elif len(playing_clients) == 1:
            playing_clients.append(player)
            await websocket.send("PLAY" + str(len(playing_clients)))
            print ("sent " + "PLAY" + str(len(playing_clients)))
        else:
            await websocket.send("ALREADY 2 PLAYERS")
            print("Already 2 players?")
            

async def home_screen(selection, client, websocket):
    print("selection " + selection)
    print("client "+ client)
    if selection == "1": #replay
        print("replay")
        if len(REPLAY_LOG) != 0:
            await websocket.send("REPLAY " + str(REPLAY_LOG[-1]))
        else: 
            await websocket.send("NO REPLAYS AVAILABLE ")
    if selection == "2": #multiplayer
        print("multiplayer")
        await multi_player_hub(client, websocket)
        print("here?")

sent = []
async def hub(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        message_state = message[0]
        if message_state == "0": #user identification
            await identify_user(message[3:], websocket)
        if message_state == "1": #new user
            await new_user(message, websocket)
        if message_state == "2": #homescreen
            index = message.find(":")
            await home_screen(message[index+1:], message[2:index-1], websocket)
        
        if message_state == "3":  # play
            update_game(message[2],  message[3:])
            myPaddle1.update()
            myPaddle2.update()
            myBall.update(myPaddle1, myPaddle2)
            print("updated")
            end = False
            if myPaddle1.score >= 3:
                print(retrieve_player(playing_clients[0]))
                await websocket.send("WIN " + retrieve_player(playing_clients[0])[0][1])
                end = True
                sent.append(1)
            if myPaddle2.score >= 3:
                print(retrieve_player(playing_clients[1]))
                await websocket.send("WIN " + retrieve_player(playing_clients[1])[0][1])
                end = True
                sent.append(1)
            if not end:
                info = [myPaddle1.x, myPaddle2.x, myBall.x, myBall.y, myPaddle1.score, myPaddle2.score]
                REPLAY_LOG[-1].append(info)
                await websocket.send(str(info))  # Send game state to client
            elif(len(sent) == 2):
                print("game end")
                myPaddle1.score = 0
                myPaddle2.score = 0
                REPLAY_LOG.append([])
                playing_clients.clear()
                print(playing_clients)
                sent.clear()

        if message_state == "4": 
            print("STATE 4")
            if len(playing_clients) == 2:
                print("STATE 4 play")
                await websocket.send("PLAY " + str(len(playing_clients)))
            else: 
                await websocket.send("WAIT " + str(len(playing_clients)))
                print("STATE 4 wait")
        if message_state == "5":
            if message[2:6] == "VERF":
                print("here")
                random_code = random.randint(10000, 99999)
                emailcode.sendEmail(random_code, clients[int(message[-1])-1])
                print(" EMAIL " + str(clients[int(message[-1])-1]))
                codes[clients[int(message[-1])-1]] = random_code
            else:
                print(message)
                index = message.find(":")
                code = message[index+2:]
                print(code)
                c = message[2:index]
                print(c)
                print("should be" + str(codes[clients[int(c)-1]]))
                if (code == str(codes[clients[int(c)-1]]) or code == "0"):
                    print(codes[clients[int(c)-1]])
                    await websocket.send("OK")
                else: 
                    await websocket.send("NO")
                    print("incorrect code")
REPLAY = [[]]
REPLAY_LOG = [[]]
start_server = websockets.serve(hub, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()