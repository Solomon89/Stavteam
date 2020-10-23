from flask import Flask


app = Flask(__name__)
app.debug = True



@app.route('/info')
def info():
    return 'info test'


from app import views
