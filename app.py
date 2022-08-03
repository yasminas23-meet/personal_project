from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCoJ-dL5dyGCRcPMutU1wuYAZ99v3Uhqtk",
  "authDomain": "personal-project-44a97.firebaseapp.com",
  "projectId": "personal-project-44a97",
  "storageBucket": "personal-project-44a97.appspot.com",
  "messagingSenderId": "405734341491",
  "appId": "1:405734341491:web:75965c1c41e0d480552306",
  "measurementId": "G-8R25CP389W",
  "databaseURL" : "https://personal-project-44a97-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():

    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('shop'))
       except:
           error = "Authentication failed"
           print(error)
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        users = {"email" : request.form['email'], "password" : request.form['password'], "name" : request.form['name'], "username" : request.form['username'], "bio" : request.form['bio']}
        db.child("users").child(login_session['user']['localId']).set(users)
        try:
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            print(error)
        return render_template("signup.html",error=error)
    return render_template("signup.html")

@app.route('/shop')
def shop():
	return render_template("shop.html")

@app.route('/cart')
def cart():
	return render_template("cart.html")

if __name__ == '__main__':
    app.run(debug=True)