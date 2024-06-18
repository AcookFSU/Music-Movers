import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="testuser",
    password="password",
)

mycursor = mydb.cursor()

mycursor.execute("USE musicMovers")
# Insert records into the users table
mycursor.execute("INSERT INTO users (username, password, joinDate, userType, userScore) VALUES ('alice', 'e99a18c428cb38d5f260853678922e03', '2024-01-01', 'listener', 100)")
mycursor.execute("INSERT INTO users (username, password, joinDate, userType, userScore) VALUES ('bob', 'ab56b4d92b40713acc5af89985d4b786', '2024-01-05', 'artist', 200)")
mycursor.execute("INSERT INTO users (username, password, joinDate, userType, userScore) VALUES ('carol', '5f4dcc3b5aa765d61d8327deb882cf99', '2024-01-10', 'moderator', 300)")

# Insert records into the songs table
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Song One', 2, 'These are the lyrics of song one.')")
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Song Two', 2, 'These are the lyrics of song two.')")
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Song Three', 2, 'These are the lyrics of song three.')")

# Insert records into the posts table
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp, postScore) VALUES (1, 1, 'This is an interpretation of song one.', 10)")
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp, postScore) VALUES (2, 3, 'This is an interpretation of song two.', 20)")
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp, postScore) VALUES (3, 1, 'This is an interpretation of song three.', 15)")



mydb.commit()
print("Successfully inserted test records!")
