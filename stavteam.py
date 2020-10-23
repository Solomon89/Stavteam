from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

from app import viewsfrom app import views