from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True



@app.route('/info')
def info():
    return render_template("info.html", user = "Stavteam")
