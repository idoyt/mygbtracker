import sqlite3

db = "mygbdatabase.db"


connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.id=113783;")
pages = cursor.fetchall()
print((pages[1])[2])
