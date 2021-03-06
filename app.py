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

#Example of using the authenticate() function
'''
hPass = hashPassword("password123")
print(authenticate("john_doe01", hPass))
'''

def hashPassword(pw):
    #assuming for this project a constant salt, not secure in the real world
    salt = b'e82feccefa6ff6521c5c0daf5d225cc5'
    
    #use pbkdf2 function to provide secure password hashing
    encrypted = pbkdf2_hmac('sha256', pw.encode('utf-8'), salt, 10000)
    return encrypted

def authenticate(username, password):
    #expects password as bytes string
    user_data = db.child("users").get().val()
    return username in user_data and user_data[username]['password'] == bytes.hex(password)

def hashVote(vt):
    #assuming for this project a constant salt, not secure in the real world
    salt = b'd00720e889aaff04349a1200a833349c'

    #use pbkdf2 function to provide secure hashing
    encrypted = pbkdf2_hmac('sha256', vt.encode('utf-8'), salt, 10000)
    return encrypted

def voteFor(username, vote):
    #check if user voted already
    user_data = db.child("users").child(username).get().val()
    if 'vote' in user_data and user_data['vote'] != "":
        return False

    #update the users vote selection data
    selectionData = {"vote": bytes.hex(hashVote(vote))}
    db.child("users").child(username).update(selectionData)

    #Increment the vote count of the chosen candidate
    numVotes = db.child("candidates").child(vote).get().val()['numVotes']
    newVoteCount = {"numVotes": (numVotes + 1)}
    db.child("candidates").child(vote).update(newVoteCount)
    return True 

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
    if voteFor(username, vote):
        return "{0} voted for: {1}".format(username, vote)
    else:
        return "{0} already voted.".format(username, vote)
    # voteFor(username, hashVote(vote))
    session.clear()
    return "{0} voted for: {1}".format(username, vote)
