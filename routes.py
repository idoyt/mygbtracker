from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title = "cool tab")

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
