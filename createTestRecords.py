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
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('F U N', 2, 'F is for friends who do stuff together<br>U is for you and me<br>N is for anywhere and anytime at all<br>Down here in the deep blue sea<br>F is for fire that burns down the whole town<br>U is for uranium, bombs<br>N is for no survivors when you<br>Plankton those thing arent what fun is all about<br>Now do it like this<br>F is for friends who do stuff to<br>Never, thats completely idiotic<br>Here, let me help you<br>F is for friends who do stuff together<br>U is for you and me<br>Try it<br>N is for anywhere and anytime at all<br>Down here in the deep blue sea<br>Wait, I dont understand this<br>I feel all tingly inside, should we stop?<br>No, thats how youre suppose to feel<br>Well, I like it, lets do it again<br>Okay<br>F is for frolick through all the flowers<br>U is for ukulele<br>N is for nose picking, sharing gum and sand licking<br>Here with my best buddy')")
mycursor.execute("INSERT INTO songs (name, artistUserId, lyrics) VALUES ('Goofy Goober', 2, '... Hey, all you Goobers<br>Its time to say howdy to your favorite undersea peanut, Goofy Goober<br>(Yeah)<br>(Yeah)<br>(Yeah)<br>... Alright, folks, this one goes out to my two bestest friends in the whole world<br>Patrick and this big peanut guy<br>Its a little ditty called<br>Goofy Goober (yeah)<br>... Oh, Im a goofy goober, yeah<br>Youre a goofy goober, yeah<br>Were all goofy goobers, yeah<br>Goofy, goofy, goober, goober, yeah (yeah)<br>Im a goofy goober, yeah<br>Youre a goofy goober, yeah<br>Were all goofy goobers, yeah<br>Goofy, goofy, goober, goober, yeah (yeah)<br>... DJ (yeah), time for the test (yeah)<br>No baby can resist singin along to this (yeah)<br>(Yeah, yeah)<br>(Yeah, yeah)<br>(Yeah, yeah)<br>... SpongeBob, its the Goofy Goober theme song<br>I know<br>... Oh, Im a goofy goober, yeah<br>Youre a goofy goober, yeah<br>Were all goofy goobers, yeah<br>Goofy, goofy, goober, goober, yeah (yeah)<br>Im a goofy goober, yeah<br>Youre a goofy goober, yeah<br>Were all goofy goobers, yeah<br>Goofy, goofy, goober, goober, yeah<br>... And heres your Triple Gooberberry Sunrise, sir<br>Ooh<br>Oh, Triple Gooberberry Sunrise, huh?<br>I guess I could use one of those<br>There you go<br>... Boy, Pat, that hit the spot<br>Im feeling better already<br>Yeah<br>Waiter, lets get another round over here<br>... Oh, Im a goofy goober, yeah<br>Youre a goofy goober, yeah<br>Were all goofy goobers, yeah<br>Goofy, goofy, goober, goober, yeah (yeah)<br>Im a goofy goober, yeah<br>Youre a goofy goober, yeah<br>Were all goofy goobers, yeah<br>Goofy, goofy, goober, goober, yeah (yeah)')")

# Insert records into the posts table
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp) VALUES (1, 1, 'This song really is a spectacle. it has not interpretation other than the interpretation of a million interpretations. Thinkign about this song alone brings tears running through my eyes, it is a wonder. When Patrick starts singing, the joy that enters my heart is inexplicable and incomporable to anything ever. I LOVE THE CAMPFIRE SONG!')")
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp) VALUES (2, 3, 'This is an interpretation of song two.')")
mycursor.execute("INSERT INTO posts (songId, authorUserId, interp) VALUES (3, 1, 'This is an interpretation of song three.')")



mydb.commit()
print("Successfully inserted test records!")
