from flask import render_template

from stavteam  import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("test.html", user = "Stavteam")
#	return "<h1>Hello, World!</h1>"
