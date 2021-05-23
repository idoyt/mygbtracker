from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
db = "mygbdatabase.db"


def do_query(query, fetch):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(query)
    if fetch == 1:
        results = cursor.fetchone()
    if fetch == 2:
        results = cursor.fetchall()
    connection.close()
    return results

@app.route('/')
def home():
    do_query("SELECT  ", 2)
    return render_template("home.html", gb = gb)

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
