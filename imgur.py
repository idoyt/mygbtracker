import urllib.request
import substring
import sqlite3
import datetime
import validators


db = "mygbdatabase.db"

connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "SELECT Photo.id, Photo.link FROM Photo" # WHERE Photo.link LIKE '%i.imgur.com/%' OR '%imgur.com/%'"
something = cursor.execute(sql)
results = something.fetchall()
connection.close()

'''for i in something:
    valid=validators.url(i[0])
    if valid==True:
        pass
    else:
        print("Invalid url", i[0])'''

for i in results:
    try:
        x = urllib.request.urlretrieve(i[1], f"static/images/{i[0]}.jpg")
    except Exception as e:
        print(i)
