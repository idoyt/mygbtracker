from flask import Flask, render_template, jsonify, request, redirect, flash, abort
import sqlite3

app = Flask(__name__)
db = "mygbdatabase.db"

def do_query(query, data = None, fetchall = False):
    # function to retrieve data from my database
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    if data is None:
        cursor.execute(query) # if there is no need to filter the data
    else:
        cursor.execute(query, data) # have to filter the data
    results = cursor.fetchall() if fetchall else cursor.fetchone()
    connection.close()
    return results

@app.route('/')
def index():
    # home page shows newest 8 threads in my database NOT ON GEEKHACK
    results = do_query("SELECT Thread.id, Photo.id, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id GROUP BY Thread.id ORDER BY Thread.start_date DESC LIMIT 8;", data = None, fetchall = True)
    return render_template("index.html", results = results, title = "Home")

@app.route('/groupbuy')
def groupbuy():
    # displays all group buy threads and their data.
    results = do_query("SELECT Thread.id, Photo.id, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=2 GROUP BY Thread.id ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    return render_template("threads.html", results = results, title = "Group Buy")

@app.route('/interestcheck')
def interestcheck():
    # displays all interest check threads and their data.
    results = do_query("SELECT Thread.id, Photo.id, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Status.id=3 GROUP BY Thread.id ORDER BY Thread.start_date DESC;", data = None , fetchall = True)
    return render_template("threads.html", results = results, title = "Interest Check")

@app.route("/thread/<int:id>")
def thread(id):
    #opens the thread info in a new page
    #gets all the relevant data from the database where the id = to the thread that it got it from.
    results = do_query("SELECT Thread.id, Starter.id, Link.link, Thread.thread_name, Starter.starter_name, Status.status_name, Thread.start_date FROM Thread JOIN Starter ON Starter.id = Thread.starter_id JOIN Status ON Status.id = Thread.status_id LEFT JOIN Link ON Thread.id = Link.thread_id WHERE Thread.id=?;",(id,), fetchall = True)
    imgs = do_query("SELECT Photo.id FROM Photo WHERE Photo.thread_id=?;",(id,), fetchall = True)
    img = [] # creates a list of images and numbers them so that the numbers on the image works.
    for i in range(1, len(imgs)+1):
        img.append(imgs[i-1] + (i,))
    return render_template("thread.html", results = results, imgs = imgs, title = (results[0])[3])

@app.route("/popup", methods=["POST"])
def popup():
    # modal popup for thread info
    if request.method == 'POST':
        # gets id from the post that user clicked.
        gbid = request.form['gbid']
        # gets data from database of the thread that the person clicks on.
        results = do_query("SELECT Thread.id, Starter.id, Link.link, Thread.thread_name, Starter.starter_name, Status.status_name, Thread.start_date FROM Thread JOIN Starter ON Starter.id = Thread.starter_id JOIN Status ON Status.id = Thread.status_id LEFT JOIN Link ON Thread.id = Link.thread_id WHERE Thread.id=?;",(gbid,), fetchall = True)
        imgs = do_query("SELECT Photo.id FROM Photo WHERE Photo.thread_id=?;",(gbid,), fetchall = True)
        img = [] # creates a list of images and numbers them so that the numbers on the image works.
        for i in range(1, len(imgs)+1):
            img.append(imgs[i-1] + (i,))
    return jsonify({'htmlresponse': render_template('threadinfo.html', results = results, img = img)})

@app.route ("/search", methods=["POST", "GET"])
def search():
    #search bar.
    if request.method == "POST":
        # uses like to search for anything like user input and group make sure there is only one box for each thread.
        results = do_query("SELECT Thread.id, Photo.link, Thread.thread_name, Status.status_name, Thread.start_date FROM Thread JOIN status ON Status.id = Thread.status_id JOIN Photo ON Thread.id = Photo.thread_id WHERE Thread.thread_name LIKE '%' || ? || '%' GROUP BY Thread.id ORDER BY Thread.thread_name;", (request.form.get("filter"),), fetchall = True)
        #error handling
        if len(results) == 0: # if no results
            return redirect ("/error")
        elif request.form.get("filter") == '': # if nothing is entered
            return redirect ('/error')
        else:
            return render_template("searchresults.html", results = results, title = "Search Results")

@app.route ("/error")
def error():
    #error page, for when user input returns no results.
    return render_template("404.html", title = "404")

@app.errorhandler(404)
def error404(error):
    # 404 error page
    return render_template('404.html', title ="404")

@app.errorhandler(405)
def error404(error):
    # 405 error page
    return render_template('405.html', title ="405")

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
