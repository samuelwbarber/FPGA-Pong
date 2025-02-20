import psycopg2

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

    # Print PostgreSQL version
    cursor.execute("SELECT * FROM USER_TBL;")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
