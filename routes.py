from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title = "cool tab")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/thing/<int:num>')
def thing(num):
  num2 = num*num
  return render_template("thing.html", num = num, num2 = num2)

# tells flask what port to run on
if __name__ == "__main__":
    app.run(debug=True, port=1111)
