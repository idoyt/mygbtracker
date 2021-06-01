from flask import Flask, render_template
from flask_modals import Modal
import sqlite3
from flask_modals import render_template_modal


app = Flask(__name__)
modal = Modal(app)
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
def live():
    results = do_query("SELECT Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id WHERE Status.id=1;", 2)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", 1)
    return render_template("home.html", results = results, number = number)

@app.route('/gb')
def upcoming():
    results = do_query("SELECT Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id WHERE Status.id=2;", 2)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", 1)
    return render_template("home.html", results = results, number = number)

@app.route('/ic')
def interestcheck():
    results = do_query("SELECT Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id WHERE Status.id=3;", 2)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", 1)
    return render_template("home.html", results = results, number = number)

@app.route('/completed')
def completed():
    results = do_query("SELECT Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id WHERE Status.id=4;", 2)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", 1)
    return render_template("home.html", results = results, number = number)

@app.route('/<int:id>')
def modal(id):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("SELECT Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.type_id WHERE Thread.id=?; ",(id,))
    id = cursor.fetchone()
    return render_template_modal("home.html", id = id, modal ='modal-form', redirect = False)

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
