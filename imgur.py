import urllib.request
import substring
import sqlite3
import datetime
import validators


db = "mygbdatabase.db"

#gets all tbe photo links
connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "SELECT Photo.id, Photo.link FROM Photo"
something = cursor.execute(sql)
results = something.fetchall()
connection.close()


# loops through the links and downloads them, naming them as the id in the database.
for i in results:
    try:
        x = urllib.request.urlretrieve(i[1], f"static/images/{i[0]}.jpg")
    except Exception as e:
        #prints it so i can save the log of the console
        print(i)
