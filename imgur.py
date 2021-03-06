import urllib.request
import substring
import sqlite3
import datetime
import validators


db = "mygbdatabase.db"

#gets all the photo links
connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "SELECT Photo.id, Photo.link FROM Photo"
something = cursor.execute(sql)
results = something.fetchall()
connection.close()


# loops through the links, downloads them, naming them as the id in the database
for i in results:
    try:
        x = urllib.request.urlretrieve(i[1], f"static/images/{i[0]}.jpg")
    except Exception as e:
        # print it, see which imgs did not download
        print(i)
