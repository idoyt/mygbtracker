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
    results = do_query("SELECT Thread.id, Photo.id, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id GROUP BY Thread.id ORDER BY Thread.start_date DESC LIMIT 8;", data = None, fetchall = True)
    return render_template("index.html", results = results, title = "Home")

@app.route('/groupbuy')
def groupbuy():
    results = do_query("SELECT Thread.id, Photo.id, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=2 GROUP BY Thread.id ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    return render_template("threads.html", results = results, title = "Group Buy")

@app.route('/interestcheck')
def interestcheck():
    results = do_query("SELECT Thread.id, Photo.id, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=3 GROUP BY Thread.id ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    return render_template("threads.html", results = results, title = "Interest Check")

@app.route("/thread/<int:id>")
def thread(id):
    results = do_query("SELECT Thread.id, Starter.id, Link.link, Thread.thread_name, Starter.starter_name, Status.status_name, Thread.start_date FROM Thread JOIN Starter ON Starter.id = Thread.starter_id JOIN Status ON Status.id = Thread.status_id LEFT JOIN Link ON Thread.id = Link.thread_id WHERE Thread.id=?;",(id,), fetchall = True)
    imgs = do_query("SELECT Photo.id FROM Photo WHERE Photo.thread_id=?;",(id,), fetchall = True)
    img = []
    for i in range(1, len(imgs)+1):
        img.append(imgs[i-1] + (i,))
    return render_template("thread.html", results = results, img = img, title = (results[0])[3])

@app.route("/ajaxfile", methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        gbid = request.form['gbid']
        results = do_query("SELECT Thread.id, Starter.id, Link.link, Thread.thread_name, Starter.starter_name, Status.status_name, Thread.start_date FROM Thread JOIN Starter ON Starter.id = Thread.starter_id JOIN Status ON Status.id = Thread.status_id LEFT JOIN Link ON Thread.id = Link.thread_id WHERE Thread.id=?;",(gbid,), fetchall = True)
        imgs = do_query("SELECT Photo.id FROM Photo WHERE Photo.thread_id=?;",(gbid,), fetchall = True)
        img = []
        for i in range(1, len(imgs)+1):
            img.append(imgs[i-1] + (i,))
    return jsonify({'htmlresponse': render_template('threadinfo.html', results = results, img = img)})

@app.route ("/search", methods=["POST", "GET"])
def search():
    #search bar.
    if request.method == "POST":
        results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.thread_name LIKE '%' || ? || '%' GROUP BY Thread.id ORDER BY Thread.thread_name;", (request.form.get("filter"),), fetchall = True)
        if len(results) == 0:
            return redirect ("/error")
        else:
            return render_template("searchresults.html", results = results, title = "Search Results")

@app.route ("/error")
def error():
    #error page, for when user input returns no results.
    return render_template("404.html", title = "404")

@app.errorhandler(404)
def error404(error):
    # note that we set the 404 status explicitly
    return render_template('404.html', title ="404")

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
