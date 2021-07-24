from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
db = "mygbdatabase.db"

def do_query(query, data = None, fetchall = False):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    results = cursor.fetchall() if fetchall else cursor.fetchone()
    connection.close()
    return results

@app.route('/')
def index():
    results = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=1 ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", data = None, fetchall = False)
    return render_template("index.html", results = results, number = number)

@app.route('/upcoming')
def upcoming():
    results = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=2 ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 2", data = None, fetchall = False)
    return render_template("index.html", results = results, number = number)

@app.route('/interestcheck')
def interestcheck():
    results = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=3 ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 3", data = None, fetchall = False)
    return render_template("index.html", results = results, number = number)

@app.route('/completed')
def completed():
    results = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=4 ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 4", data = None, fetchall = False)
    return render_template("index.html", results = results, number = number)

@app.route("/ajaxfile", methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        gbid = request.form['gbid']
        modal = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.type_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.id=?; ",(gbid,), fetchall = True)
    return jsonify({'htmlresponse': render_template('modal.html', modal = modal)})



# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
