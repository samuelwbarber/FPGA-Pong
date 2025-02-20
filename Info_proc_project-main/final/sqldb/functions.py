# adapt to PostgreSQL
import psycopg2 
import time

# check if player exists in USER_TBL table
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
    sql = "INSERT INTO USER_TBL (Email, firstName, ColourR, ColourG, ColourB, IndexIcon) VALUES ('"+Email+"','"+firstName+"', 0, 0, 0, 0);"
    cursor.execute(sql)
    connection.commit()

# update player score in USER_TBL table
def update_score(ScoreInc, Email):
    sql = "UPDATE USER_TBL SET Score = Score + "+str(ScoreInc)+" WHERE Email = '"+Email+"';"
    cursor.execute(sql)
    connection.commit()

# save game by providing players' emails and GameState (string)
def save_game(Email0, Email1, GameState):
    Timestamp = int(time.time())
    sql = "INSERT INTO SAVEGAME (Email0, Email1, Timestamp, GameState) VALUES ('"+Email0+"','"+Email1+"',"+str(Timestamp)+",'"+GameState+"');"
    cursor.execute(sql)
    connection.commit()

# replay game by providing player's email
def replay_game(Email0, Email1):
    sql = "SELECT GameState FROM SAVEGAME WHERE Email0 = '"+Email0+"' OR Email1 = '"+Email1+"' ORDER BY Timestamp DESC LIMIT 1;"
    cursor.execute(sql)
    game = cursor.fetchone()
    if game:
        return game[0]
    else:
        return None

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

    # Use the functions

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)