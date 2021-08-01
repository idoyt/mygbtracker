import urllib.request
import substring
import sqlite3
import datetime
import validators


db = "mygbdatabase.db"

connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "SELECT Photo.link FROM Photo WHERE Photo.link LIKE '%i.imgur.com/%' OR '%imgur.com/%'"
something = cursor.execute(sql)

for i in something:
    valid=validators.url(i[0])
    if valid==True:
        pass
    else:
        print("Invalid url", i[0])

#x = substring.substringByChar(y, startChar="m", endChar = "")
#x2 = substring.substringByChar(x, startChar=".", endChar = "")
#urllib.request.urlretrieve("https://i.imgur.com/MkrsTSL.png", f"static/images/{x2[5:]}")
