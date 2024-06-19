import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="testuser",
    password="password",
)

mycursor = mydb.cursor()

mycursor.execute("USE musicMovers")
# Insert records into the users table
mycursor.execute("INSERT INTO users (username, password, joinDate, userType) VALUES ('alice', 'e99a18c428cb38d5f260853678922e03', '2024-01-01', 'listener')")
mycursor.execute("INSERT INTO users (username, password, joinDate, userType) VALUES ('Spongebob', 'ab56b4d92b40713acc5af89985d4b786', '2024-01-05', 'artist')")
mycursor.execute("INSERT INTO users (username, password, joinDate, userType) VALUES ('carol', '5f4dcc3b5aa765d61d8327deb882cf99', '2024-01-10', 'moderator')")

# Insert records into the songs table
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Campfire Song', 2, 'Intro: SpongeBob<br>I call this one the Campfire Song Song<br>Lets gather around the campfire<br>And sing our campfire song<br>Our C-A-M-P-F-I-R-E S-O-N-G song<br>And if you dont think that we can sing it faster, then youre wrong<br>But itll help if you just sing along<br><br>Bridge: Patrick<br>Bom, bom, bom<br><br>Verse: SpongeBob & Patrick<br>C-A-M-P-F-I-R-E S-O-N-G song<br>C-A-M-P-F-I-R-E S-O-N-G song<br>And if you dont think that we can sing it faster, then youre wrong<br>But itll help if you just sing along<br>C-A-M-P-F-I-R-E S-O-N-G song<br>Patrick!<br>Song! C-A-M-P-F-I-R-E<br>Squidward!<br>Good!<br><br>Outro: SpongeBob<br>Itll help<br>Itll help<br>If you just sing along!<br>Oh yeah!')")
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Song Two', 2, 'These are the lyrics of song two.')")
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Song Three', 2, 'These are the lyrics of song three.')")

# Insert records into the posts table
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp) VALUES (1, 1, 'This is an interpretation of song one.')")
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp) VALUES (2, 3, 'This is an interpretation of song two.')")
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp) VALUES (3, 1, 'This is an interpretation of song three.')")



mydb.commit()
print("Successfully inserted test records!")
