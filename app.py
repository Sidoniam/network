from flask import Flask, render_template, request, url_for, redirect, session
import pyrebase
from hashlib import pbkdf2_hmac

#see https://github.com/thisbejim/Pyrebase for pybase api
config = {
    "apiKey": "AIzaSyClQ-JVkX6calAWG9HQwIpJqUYKgrIEhcU",
    "authDomain": "digital-voting-project.firebaseapp.com",
    "databaseURL": "https://digital-voting-project-default-rtdb.firebaseio.com",
    "storageBucket": "digital-voting-project.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Obtaining the data, and setting the vote count example
'''
admins = db.child("admins").get()
users = db.child("users").get()
candidates = db.child("candidates").get()

data = {"numVotes": "0"}
db.child("candidates").child("Donald Trump").set(data)
db.child("candidates").child("Joe Biden").set(data)

print(admins.val())
print(users.val())
print(candidates.val())
'''


def hashPassword(pw):
    #assuming for this project a constant salt, not secure in the real world
    salt = b'e82feccefa6ff6521c5c0daf5d225cc5'
    
    #use pbkdf2 function to provide secure password hashing
    encrypted = pbkdf2_hmac('sha256', pw.encode('utf-8'), salt, 10000)
    return encrypted

def authenticate(username, password):
    user_data = db.child("users").get()[username]
    return user_data['password'] == password

def hashVote(vt):
    #assuming for this project a constant salt, not secure in the real world
    salt = b'd00720e889aaff04349a1200a833349c'

    #use pbkdf2 function to provide secure hashing
    encrypted = pbkdf2_hmac('sha256', vt.encode('utf-8', salt, 10000))
    return encrypted

def voteFor(username, vote):
    pass


app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def handleData():
    username = request.form.get('username')
    password = request.form.get('password')
    password = hashPassword(password)
    if(authenticate(username, password)):
        session['username'] = username
        return redirect(url_for('submitVote'))
    else:
       return "Invalid Credentials. Refresh the page and try again!"

@app.route('/vote')
def submitVote():
    return render_template('vote.html')

@app.route('/vote', methods=['POST'])
def handleVote():
    vote = request.form.get('vote')
    username = session['username']
    # voteFor(username, hashVote(vote))
    # session.clear()
    return "{0} voted for: {1}".format(username, vote)
