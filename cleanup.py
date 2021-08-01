import sqlite3
import datetime

db = "mygbdatabase.db"

connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Thread.id, Thread.status_id, Thread.start_date FROM Thread")
clean = cursor.fetchall()

for i in clean:
    if "2021-01-01" > i[2]:
        sql = "UPDATE Thread SET status_id = 4 WHERE Thread.id = ?;"
        cursor.execute(sql, (i[0],))
        connection.commit()


connection.close()
