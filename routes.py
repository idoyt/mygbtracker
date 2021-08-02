from flask import Flask, render_template, jsonify, request, redirect, flash
import sqlite3

app = Flask(__name__)
db = "mygbdatabase.db"
app.secret_key = "and"


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
    return render_template("index.html") #, results = results, number = number)

@app.route('/groupbuy')
def groupbuy():
    results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=2 GROUP BY Thread.id ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    return render_template("threads.html", results = results)

@app.route('/interestcheck')
def interestcheck():
    results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=3 GROUP BY Thread.id ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    return render_template("threads.html", results = results)

@app.route("/thread/<int:id>")
def thread(id):
    results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.id=?; ",(id,), fetchall = True)
    return render_template("thread.html", results = results)

@app.route("/ajaxfile", methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        gbid = request.form['gbid']
        results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.id=?; ",(gbid,), fetchall = True)
    return jsonify({'htmlresponse': render_template('modal.html', results = results)})

@app.route ("/search", methods=["POST", "GET"])
def search():
    #search bar, allows user to search for a specific herb and redirects them to the specific page for that herb.
    if request.method == "POST":
        print (request.form.get("filter"))
        results = do_query("SELECT * FROM Thread WHERE Thread.thread_name LIKE '%' || ? || '%' ORDER BY Thread.thread_name;", (request.form.get("filter"),), fetchall = True)
        if results == None:
            return redirect ("/error")
        else:
            return redirect (f"/thread/{(results[0])[0]}")

@app.route ("/error")
def error():
    #error page, for when user input returns no results.
    return render_template("error.html")

@app.route ("/searchresults")
def searchresults():
    return render_template("searchresults.html", title = "Search Results")

@app.errorhandler(404)
def error404(error):
    # note that we set the 404 status explicitly
    return render_template('404.html')

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
