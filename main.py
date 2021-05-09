from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = None
import api

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/testcrash")
def testcrash():
    raise Exception("Test Exception")
