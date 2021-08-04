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
    newest = do_query("SELECT Thread.start_date FROM Thread ORDER BY Thread.start_date DESC;", data = None , fetchall = False)
    results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.start_date = ? GROUP BY Thread.id ORDER BY Thread.start_date DESC;", (newest[0],), fetchall = True)
    return render_template("index.html", results = results)

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
    #search bar.
    if request.method == "POST":
        print (request.form.get("filter"))
        results = do_query("SELECT * FROM Thread WHERE Thread.thread_name LIKE '%' || ? || '%' ORDER BY Thread.thread_name;", (request.form.get("filter"),), fetchall = True)
        if results == None:
            return redirect ("/error")
        else:
            return render_template("searchresults.html", results = results, title = "Search Results")

@app.route ("/error")
def error():
    #error page, for when user input returns no results.
    return render_template("error.html")

@app.errorhandler(404)
def error404(error):
    # note that we set the 404 status explicitly
    return render_template('404.html')

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
