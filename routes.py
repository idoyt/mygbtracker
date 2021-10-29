from flask import Flask, render_template, jsonify, request, flash, abort
import sqlite3

app = Flask(__name__)
db = "mygbdatabase.db"


def do_query(query, data=None, fetchall=False):
    # function to retrieve data from my database
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    if data is None:
        # if there is no need to filter the data
        cursor.execute(query)
    else:
        # have to filter the data
        cursor.execute(query, data)
    #fetchall when fetchall is true
    results = cursor.fetchall() if fetchall else cursor.fetchone()
    connection.close()
    return results


@app.route('/')
def index():
    # home page shows newest 8 threads in MY database
    thread_info = do_query("""SELECT Thread.id, Photo.id, Thread.thread_name,
                       Category.category_name, Thread.start_date
                       FROM Thread
                       JOIN Category ON Category.id = Thread.category_id
                       JOIN Photo ON Thread.id = Photo.thread_id
                       GROUP BY Thread.id ORDER BY Thread.start_date
                       DESC LIMIT 8;""", fetchall=True)
    return render_template("index.html", thread_info=thread_info, title="Home")


@app.route('/groupbuy')
def groupbuy():
    # query to get all data to display all group buy threads information.
    thread_info = do_query("""SELECT Thread.id, Photo.id, Thread.thread_name,
                       Category.category_name,Thread.start_date
                       FROM Thread
                       JOIN Category ON Category.id = Thread.category_id
                       JOIN Photo ON Thread.id = Photo.thread_id
                       WHERE Category.id=2
                       GROUP BY Thread.id
                       ORDER BY Thread.start_date DESC;""", fetchall=True)
    return render_template("threads.html", thread_info=thread_info,
                           title="Group Buy")


@app.route('/interestcheck')
def interestcheck():
    # query to get all data to display all ginterest check threads information.
    thread_info = do_query("""SELECT Thread.id, Photo.id, Thread.thread_name,
                       Category.category_name, Thread.start_date
                       FROM Thread
                       JOIN Category ON Category.id = Thread.category_id
                       JOIN Photo ON Thread.id = Photo.thread_id
                       WHERE Category.id=3 GROUP BY Thread.id
                       ORDER BY Thread.start_date DESC;""", fetchall=True)
    return render_template("threads.html", thread_info=thread_info,
                           title="Interest Check")


@app.route("/popup", methods=["POST"])
def popup():
    # modal popup for thread info
    # recieves id of container that the user clicked.
    id = request.form['id']
    # gets all data for the thread that the user clicks on.
    thread_info = do_query("""SELECT Thread.id, Starter.id, Link.link,
                       Thread.thread_name,Starter.starter_name,
                       Category.category_name, Thread.start_date
                       FROM Thread
                       JOIN Starter ON Starter.id = Thread.starter_id
                       JOIN Category ON Category.id = Thread.category_id
                       LEFT JOIN Link ON Thread.id = Link.thread_id
                       WHERE Thread.id=?;""",
                       (id,), fetchall=True)
    # get all images which are related to the thread.
    imgs = do_query("""SELECT Photo.id
                    FROM Photo
                    WHERE Photo.thread_id=?;""",
                    (id,), fetchall=True)
    # numbers all images from 1 - x.
    # creates a list [(images, number,)]
    # slideshow js needs this to work also needed to show which image you're on
    imgs_with_number = []
    for i in range(1, len(imgs)+1):
        imgs_with_number.append(imgs[i-1] + (i,))
    imgs = imgs_with_number
    return jsonify({'htmlresponse': render_template('threadinfo.html',
                   thread_info=thread_info, imgs=imgs, popup=True)})


@app.route("/search", methods=["POST"])
def search():
    # searchbar.
    # searches for anything that is similar to whatever the user inputted.
    thread_info = do_query("""SELECT Thread.id, Photo.id, Thread.thread_name,
                       Category.category_name, Thread.start_date
                       FROM Thread
                       JOIN category ON Category.id = Thread.category_id
                       JOIN Photo ON Thread.id = Photo.thread_id
                       WHERE Thread.thread_name
                       LIKE '%' || ? || '%'
                       GROUP BY Thread.id
                       ORDER BY Thread.thread_name;""",
                       (request.form.get("filter"),), fetchall=True)
    return render_template("searchresults.html", thread_info=thread_info,
                           no_thread_info=len(thread_info),
                           title="Search Results")


@app.errorhandler(404)
def error404(error):
    # 404 error page
    return render_template('404.html', title="404")


@app.errorhandler(405)
def error404(error):
    # 405 error page
    return render_template('405.html', title="405")

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=False, port=1111)
