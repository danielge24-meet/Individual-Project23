from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
"apiKey": "AIzaSyDZiqrmVVGxa2cjwl2dKsUQASPABzJSkao",
  "authDomain": "memory-gram-6c1ff.firebaseapp.com",
  "projectId": "memory-gram-6c1ff",
  "storageBucket": "memory-gram-6c1ff.appspot.com",
  "messagingSenderId": "598232570272",
  "appId": "1:598232570272:web:285a798f7b9d09273aecc5",
  "databaseURL": "https://memory-gram-6c1ff-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username=request.form['username']
        bio=request.form['bio']
        pfp = "https://static.vecteezy.com/system/resources/previews/002/534/006/original/social-media-chatting-online-blank-profile-picture-head-and-body-icon-people-standing-icon-grey-background-free-vector.jpg"

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            user={"email":email,"password":password,"username":username,"bio":bio,"pfp":pfp}
            UID=login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('profile'))
        except:
            return redirect(url_for('signup'))
    return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('profile'))
        except:
            return redirect(url_for('signup'))
    return render_template("signup.html")




@app.route('/add_memory', methods=['GET', 'POST'])
def add_memory():
    if request.method == 'POST':
        img=request.form['image']
        title=request.form['title']
        text=request.form['text']
        uid=login_session['user']['localId']
        memory={"title":title,"text":text,"image":img,"uid":uid}
        try:
            db.child("memories").child(uid).set(memory)
            return redirect(url_for('all_memories'))
        except Exception as e:
            print(e)
    return render_template("add_memory.html")

@app.route('/change',methods=['GET', 'POST'])
def change():
    if request.method == 'POST':
        username=request.form['username']
        bio=request.form['bio']
        pfp = request.form['pfp']


        try:
            UID = login_session['user']['localId']
            changed_user={"username":username,"bio":bio,"pfp":pfp}
            db.child("Users").child(UID).update(changed_user)
            return redirect(url_for('profile'))  
        except:
            return redirect(url_for('change'))
    return render_template("change.html")




@app.route('/all_of_memories',methods=['GET', 'POST'])
def all_memories():
    UID=login_session['user']['localId']
    all_of_memories=db.child("memories").child(UID).get().val()
    return render_template("all_memories.html", p=all_of_memories)


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    UID= login_session['user']['localId']
    user_profile=db.child("Users").child(UID).get().val()
    return render_template("profile.html",username=user_profile["username"], bio=user_profile["bio"], pfp=user_profile["pfp"])

if __name__ == '__main__':
    app.run(debug=True)