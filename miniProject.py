from flask import Flask, render_template, request, session
import pyrebase
import json

app = Flask(__name__)

app.config['SECRET_KEY'] ='b1gk3y'

app.static_folder = 'static'

#configure initial firebase settings
#config = {
 # "apiKey": "AIzaSyDSdsT2h6wAlkQI3rj7sAbPD2a0hFJVIIA",
 # "authDomain": "mathtutorapp-f3ddc.firebaseapp.com",
 # "databaseURL": "https://mathtutorapp-f3ddc.firebaseio.com",
 # "storageBucket": "mathtutorapp-f3ddc.appspot.com"
#}

#use pYrebase package to use firebase through python and flask
#firebase = pyrebase.initialize_app(config)

#auth = firebase.auth()
#db = firebase.database()

@app.route("/", methods = ['POST','GET'])
def login():
    return render_template('login.html')

@app.route("/home", methods = ['POST','GET'])
def home():
    return render_template('home.html')

@app.route("/help", methods = ['POST','GET'])
def help():
    return render_template('seekhelp.html')

@app.route("/tips", methods = ['POST','GET'])
def tips():
    return render_template('tips.html')

if __name__ == '__main__':
    app.run(debug=True)
