from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
db = "mygbdatabase.db"
#index_page_query = (f"SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id{status_id} ORDER BY Thread.start_date DESC;")


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
    #results = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=1 ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    #number = do_query("SELECT Thread.id FROM Thread WHERE Thread.status_id = 1", data = None, fetchall = False)
    return render_template("index.html")

@app.route("/ajaxfile", methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        gbid = request.form['gbid']
        modal = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.type_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.id=?; ",(gbid,), fetchall = True)
    return jsonify({'htmlresponse': render_template('modal.html', modal = modal)})

"""@app.route('/nav', methods=["POST","GET"])
def nav():
    if request.method == 'POST':
        typeid = request.form['typeid']
        nav = do_query("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=2 ORDER BY Thread.start_date DESC;", data = None , fetchall = True")
        return jsonify({"")})"""

@app.route('/search', methods = ["POST","GET"])
def search():
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    if request.method == 'POST':
         search_word = request.form['query']
         print(search_word)
         if search_word == '':
             query = ("SELECT Thread.id, Photo.photo_link, Thread.thread_name, Status.status_name, Type.type_name, Thread.price, Thread.start_date, Thread.end_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Type ON Type.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=1 ORDER BY Thread.start_date DESC;")
             cur.execute(query)
             results = cur.fetchall()
         else:
             query = (f"SELECT * FROM Thread WHERE Thread.thread_name LIKE '%{search_word}%' ORDER BY Thread.thread_name;")
             cur.execute(query)
             numrows = int(cur.rowcount)
             results = cur.fetchall()
             print(numrows)
    return jsonify({'htmlresponse': render_template('wrapper.html', results=results, numrows=numrows)})



# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
