from flask import Flask, render_template, request, url_for, redirect, session
app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def handleData():
    username = request.form.get('username')
    password = request.form.get('password')
    # password = hashPassword(password)
    # if(authenticate(username, password)):
    session['username'] = username
    return redirect(url_for('submitVote'))
    # else:
    #    return "Invalid Credentials. Refresh the page and try again!"

@app.route('/vote')
def submitVote():
    return render_template('vote.html')

@app.route('/vote', methods=['POST'])
def handleVote():
    vote = request.form.get('vote')
    # vote(hashVote(vote), session['username'])
    # session.clear()
    return "{0} voted for: {1}".format(session['username'], vote)
    
