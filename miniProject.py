from flask import Flask, render_template, request, session
from datetime import date
import pyrebase
import json

app = Flask(__name__)

app.config['SECRET_KEY'] ='b1gk3y'

app.static_folder = 'static'

#configure initial firebase settings
config = {
  "apiKey": "AIzaSyB9Ukcx2PNG9FSkhGbW4YH7lXiC6tlBCcQ",
  "authDomain": "authentication-78acc.firebaseapp.com",
  "databaseURL": "https://authentication-78acc.firebaseio.com",
  "storageBucket": "authentication-78acc.appspot.com"
}

#use pYrebase package to use firebase through python and flask
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()

@app.route("/", methods = ['POST','GET'])
def login():
    return render_template('login.html')

@app.route("/home", methods = ['POST','GET'])
def home():
    return render_template('home.html')

@app.route("/complete", methods = ['POST', 'GET'])
def complete():
    today = date.today()
    q1 = int(request.form.get("Q1"))
    q2 = int(request.form.get("Q2"))
    q3 = int(request.form.get("Q3"))
    q4 = int(request.form.get("Q4"))
    q5 = int(request.form.get("Q5"))
    q6 = int(request.form.get("Q6"))
    q7 = int(request.form.get("Q7"))
    q8 = int(request.form.get("Q8"))
    answer = [q1, q2, q3, q4, q5, q6, q7, q8]
    print(today)
    print(answer)
    return render_template('complete.html')

@app.route("/help", methods = ['POST','GET'])
def help():
    return render_template('seekhelp.html')

@app.route("/tips", methods = ['POST','GET'])
def tips():
    return render_template('tips.html')

if __name__ == '__main__':
    app.run(debug=True)
