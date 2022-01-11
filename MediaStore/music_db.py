import mysql.connector


class MusicDb:

    def init(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Moditha@1996",
            database="database_01"
        )


        self.mycursor = self.mydb.cursor()
        self.createsongstable()

    # create table
    def createsongstable(self):
        createtablequery = "CREATE TABLE IF NOT EXISTS song (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(250), name VARCHAR(255), emotion VARCHAR(50))"

        self.mycursor.execute(createtablequery)
        # self.conn.commit()
        print("table")

    # drop a table
    def dropsongstable(self):
        dropquery = 'DROP TABLE song;'
        self.mycursor.execute(dropquery)
        self.myresult = self.mycursor.fetchall()

    def clearsongstable(self):
        deletequery = 'DELETE FROM song;'
        self.mycursor.execute(deletequery)
        self.myresult = self.mycursor.fetchall()

    # insert a song
    def insertsong(self, url, name, emotion):
        insertquery = "INSERT INTO song (url,name,emotion) VALUES (%s,%s,%s)"
        val = (url, name, emotion)
        self.mycursor.execute(insertquery, val)
        self.mydb.commit()
        print("Song successfully added")

    # get all songs from database
    def getallsongs(self):
        selectquery = 'SELECT url FROM song'
        self.mycursor.execute(selectquery)
        self.myresult = self.mycursor.fetchall()
        return self.myresult

    # get a song from the database which was given by user
    def getSong(self, x):
        self.mycursor.execute("SELECT name FROM song WHERE name=%s", (x,))
        self.myresult = self.mycursor.fetchall()
        return self.myresult

    # get list of happy songs
    def getsongsforHappy(self):
        selectQuery = "SELECT url FROM song WHERE emotion='happy'"
        self.mycursor.execute(selectQuery)
        self.myresult = self.mycursor.fetchall()
        return self.myresult

    # get list of sad songs
    def getsongsforSad(self):
        selectQuery = "SELECT url FROM song WHERE emotion='sad'"
        self.mycursor.execute(selectQuery)
        self.myresult = self.mycursor.fetchall()
        return self.myresult

    # get list of calm songs
    def getsongsforCalm(self):
        selectQuery = "SELECT url FROM song WHERE emotion='calm'"
        self.mycursor.execute(selectQuery)
        self.myresult = self.mycursor.fetchall()
        return self.myresult

    # close db connection
    def close(self):
        self.mydb.commit()
        # self.conn.close()