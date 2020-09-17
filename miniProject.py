from flask import Flask, render_template, request, session
from datetime import date
import pyrebase
import json
import requests

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

#signin function using pyrebase
def signIn(email,password):
	user = auth.sign_in_with_email_and_password(email,password)
	return user

#signup function using pyrebase
def signUp(email,password):
    auth.create_user_with_email_and_password(email,password)

#symptoms class to store survey info
class symptoms:
    def __init__(self, fever = 0, cough = 0, nose = 0, loss = 0, sob = 0, throat = 0, vomit = 0, ache = 0):
        self.fever = fever
        self.cough = cough
        self.nose = nose
        self.loss = loss
        self.sob = sob
        self.throat = throat
        self.vomit = vomit
        self.ache = ache

#covid stats class to store covid api info
class covidStats:
    def __init__(self, positive, new, negative, recovered, deaths, newDeaths):
        self.positive = positive
        self.new = new
        self.negative = negative
        self.recovered = recovered
        self.deaths = deaths
        self.newDeaths = deaths

#initialize symptom count for the day to 0
today = date.today()
initSymptoms = symptoms()
y = json.dumps(initSymptoms.__dict__)

db.child("adminDashboard").child(today).child("completedSurveys").set(0)
db.child("adminDashboard").child(today).child("symptomTally").set(y)

#all routed pages
@app.route("/", methods = ['POST','GET'])
def login():
    return render_template('login.html')

@app.route("/home", methods = ['POST','GET'])
def home():
    #login with firebase
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = signIn(email,password)
        session['user'] = user
        username = email.split('@')[0].lower()
        session['username'] = username
        return render_template('home.html', username = username)
    else:
        return render_template('home.html')

#get email and password and push to database to create usernames
@app.route("/signup", methods = ['POST','GET'])
def signup():
    email = request.form.get("email1")
    password = request.form.get("password1")
    admin = request.form.get("admin")
    signUp(email,password)
    username = email.split('@')[0].lower()
    db.child("users").child(username).child("admin").set(admin)
    return render_template('signup.html')

@app.route("/complete", methods = ['POST', 'GET'])
def complete():
    #get survey info and push to database for dashboard and symptom tracking
    username = session.get('username')
    today = date.today()
    tally = db.child("adminDashboard").child(today).child("completedSurveys").get().val()
    tally += 1
    symptomTotal = db.child("adminDashboard").child(today).child("symptomTally").get().val()
    symptomTotal = json.loads(symptomTotal)

    q1 = int(request.form.get("Q1"))
    symptomTotal["fever"] += q1 
    q2 = int(request.form.get("Q2"))
    symptomTotal["cough"] += q2
    q3 = int(request.form.get("Q3"))
    symptomTotal["nose"] += q3
    q4 = int(request.form.get("Q4"))
    symptomTotal["loss"] += q4
    q5 = int(request.form.get("Q5"))
    symptomTotal["sob"] += q5
    q6 = int(request.form.get("Q6"))
    symptomTotal["throat"] += q6
    q7 = int(request.form.get("Q7"))
    symptomTotal["vomit"] += q7
    q8 = int(request.form.get("Q8"))
    symptomTotal["ache"] += q8

    s = symptoms(q1, q2, q3, q4, q5, q6, q7, q8)

    y = json.dumps(s.__dict__)
    db.child("users").child(username).child(today).set(y)
    db.child("adminDashboard").child(today).child("completedSurveys").set(tally)
    y = json.dumps(symptomTotal)
    db.child("adminDashboard").child(today).child("symptomTally").set(y)
    return render_template('complete.html')

@app.route("/seekhelp", methods = ['POST','GET'])
def help():
    return render_template('seekhelp.html')

@app.route("/tips", methods = ['POST','GET'])
def tips():
    return render_template('tips.html')

#get coronavirus api and stats from database for dashboard
@app.route("/dashboard", methods = ['POST', 'GET'])
def dashboard():
    username = session.get('username')
    flag = int(db.child("users").child(username).child("admin").get().val())

    response = requests.get("https://api.covidtracking.com/v1/us/current.json")
    statsUS = covidStats(response.json()[0]['positive'], response.json()[0]['positiveIncrease'], response.json()[0]['negative'], response.json()[0]['recovered'], response.json()[0]['death'], response.json()[0]['deathIncrease'])

    response = requests.get("https://api.covidtracking.com/v1/states/ma/current.json")
    statsMA = covidStats(response.json()['positive'], response.json()['positiveIncrease'], response.json()['negative'], response.json()['recovered'], response.json()['death'], response.json()['deathIncrease'])

    if(flag == 1):
        tally = db.child("adminDashboard").child(today).child("completedSurveys").get().val()
        symptomTotal = db.child("adminDashboard").child(today).child("symptomTally").get().val()
        symptomTotal = json.loads(symptomTotal)
        return render_template('admindashboard.html', tally = tally, symptomTotal = symptomTotal, statsUS = statsUS, statsMA = statsMA)
    else:
        return render_template('dashboard.html',  statsUS = statsUS, statsMA = statsMA)

if __name__ == '__main__':
    app.run(debug=True)
