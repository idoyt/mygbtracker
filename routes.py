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
    results = do_query("SELECT Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id WHERE Status.id=1;", 2)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", 1)
    return render_template("home.html", results = results, number = number)

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
