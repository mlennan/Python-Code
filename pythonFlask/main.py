from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from passlib.hash import sha256_crypt
import mysql.connector as mariadb
import os
import operator
app = Flask(__name__)
mariadb_connect = mariadb.connect(user='chooseAUserName', password='chooseAPassword', database='Login')
@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
  login = request.form

  userName = login['username']
  password = login['password']

  cur = mariadb_connect.cursor(buffered=True)

  data = cur.execute("SELECT * FROM Login WHERE username=%s", (userName,))
  data = cur.fetchone()[2]

  if sha256_crypt.verify(password, data):
    account = True
  else:
    account = False

  if account:
    session['logged_in'] = True
  else:
    flash('wrong password!')
  return home()

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

@app.route('/pokerstart')
def poker_start():
  if not session.get('logged_in'):
    return home()
  else:
    return render_template('pokerstart.html')

@app.route('/pokerDataSend', methods=['POST', 'GET'])
def pokerSendData():
  difficulty = request.form
  email = difficulty['difficulty']
  cur = mariadb_connect.cursor(buffered=True)
  cur.execute("UPDATE Login SET email=%s WHERE username = 'me'", (email,))
  return render_template('pokerstart.html')

  # data = cur.execute("SELECT email FROM Login WHERE username='me'")
  # data = cur.fetchone()
  # return render_template('pokerdisplay.html', data=data)


@app.route('/pokerdisplay', methods=['GET'])
def poker_display():
  if not session.get('logged_in'):
    return home()
  else:
    cur = mariadb_connect.cursor(buffered=True)
    userName = "me"
    data = cur.execute("SELECT email FROM Login WHERE username=%s", (userName,))
    data = cur.fetchone()

    return render_template('pokerdisplay.html', data=data)


if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=False,host='0.0.0.0', port=5000)

#'NoneType' object is not subscriptable
#ValueError: Could not process parameters