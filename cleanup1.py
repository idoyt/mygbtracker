import sqlite3
import datetime

db = "mygbdatabase.db"

connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Starter.id FROM Starter WHERE Starter.id NOT IN(SELECT Thread.starter_id FROM Thread);")
clean = cursor.fetchall()
print (clean)

for i in clean:
    sql = "DELETE FROM Starter WHERE Starter.id = ?;"
    cursor.execute(sql, (i[0],))
    connection.commit()
connection.close()
