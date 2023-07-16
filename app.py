from flask import Flask , render_template , request , redirect , session , flash
from cs50 import SQL
from pytube import YouTube , extract
from werkzeug.security import check_password_hash, generate_password_hash
import os
from helpers import makefile,check_password_pattern , check_email_pattern , findfile , audiovideo
from flask_session import Session





db = SQL('sqlite:///music.db')
app = Flask(__name__)

key = os.urandom(12).hex()
app.secret_key = key
app.config['SECRET_KEY'] = key
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

 



@app.route('/' , methods=["POST", "GET"])
def download():
    session['video_id'] = ''
    if request.method == 'POST':
        videolink = request.form.get('InputVideo')
        try:
            id = extract.video_id(videolink)
        except:
            flash('Type in a proper youtube URL')
            return redirect('/')
        
        yt = YouTube(videolink)
        session['video_id'] = id
        return redirect('/downloading')

       
    return render_template('download.html' , yt1='')


@app.route('/downloading' , methods=["POST" , "GET"])
def downloading():
    if 'video_id' not in session:
        return redirect('/')
    id = session['video_id']
    videolink = 'https://www.youtube.com/embed/{id1}'.format(id1=id)
    yt = YouTube(videolink)
    if request.method == 'POST':
        type = request.form.get('CheckBox')
        if type not in ['audio' , 'video']:
            flash('Wrong Format')
            return redirect('/downloading')
        if type == 'audio':
            video = yt.streams.filter(only_audio=True).first()
            
        else:
            video = yt.streams.get_highest_resolution()

        path = request.form.get('path')
        if path not in ['local' , 'saved']:
            flash('Wrong Path')
            return redirect('/downloading')
        
        destination = audiovideo(type)
        outputfile = video.download( output_path=destination)
        if type=='audio':
            base , ext = os.path.splitext(outputfile)
            new_file = base + '.mp3'
            try:
                os.rename(outputfile, new_file)
                outputfile = new_file
            except :
                 flash('Could not download')

        db.execute('INSERT INTO history (user_id,time,video_title,video_url,thumbnail) VALUES (?,datetime(),?,?,?);',session['user'],yt.title,videolink,yt.thumbnail_url)
        flash('Downloaded')
        return redirect('/')  
    
    return render_template('downloading.html', id=id)


@app.route('/register' , methods=['POST' , 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash("Enter a name please!")
            return redirect('/register')
        
        name_validate = db.execute('SELECT * FROM users WHERE name = ?;', name)
        if len(name_validate) != 0:
            if len(name_validate) > 1 or name == name_validate[0]['name']:
                flash('Username already exists!')
                return redirect('/register')

        
        password = request.form.get('password')
        is_password = check_password_pattern(password)

        if not password:
            flash("Enter a password please!")
            return redirect('/register')
        
        if not is_password:
            flash("Invalid Password")
            return redirect('/register')
        
        confirm = request.form.get('confirm')
        if not confirm:
            flash("Confirm your password please!")
            return redirect('/register')
        
        if confirm != password:
            flash("Passwords don't match!")
            return redirect('/register')
        
        email = request.form.get('email')

        is_email = check_email_pattern(email)
        if not is_email:
            flash('Invalid email')
            return redirect('/register')
        


        hash = generate_password_hash(password)
        db.execute('INSERT INTO users (name , password , hash,email) VALUES (?,?,?,?)',name , password , hash,email)
        
        id = db.execute('SELECT * FROM users WHERE name = ?;' , name)
        session['user']= id[0]['id']
        session['name'] = name
        flash('Registered and logged in!')
        return redirect('/')
        
    return render_template('register.html')

@app.route('/login', methods=['POST' , 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash("Please write in a username")
            return redirect('/login')
        password = request.form.get('password')
        if not password:
            flash('Please type in a password')
            return redirect('/login')
        
        check = db.execute('SELECT * from users WHERE name=?',name)
        if len(check) == 0:
            flash("Username doesn't exist")
            return redirect('/login')
        if check[0]['name'] != name:
            flash('Wrong Username')
            return redirect('/login')
        

        password = request.form.get('password')
        if not password:
            flash('Please type in a password')
            return redirect('/login')
        if check_password_hash(check[0]['hash'],password) == False:
            flash('Wrong password!')
            return redirect('/login')
        
        session['user'] = check[0]['id']
        session['name'] = check[0]['name']
        flash('Logged in!')
        return redirect('/')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    print(session)
    if 'user' not in session:
        return redirect('/login')
    if session['user'] :
        id = session['user']
        session.pop('user',None)
        session.pop('name',None)
        
    
    if id:
        flash('Logged out!')
    return redirect('/login')



@app.route('/change',methods=['GET','POST'])
def ChangePassword():
    if request.method == 'POST':
        name = request.form.get('name')
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')
        newpasswordc = request.form.get('newpasswordc')
        if not name:
            flash('Please write a name')
            return redirect('/change')
        if not oldpassword:
            flash('Write your old password')
            return redirect('/change')
        if not newpassword:
            flash('Write your new password')
            return redirect('/change')
        if not newpasswordc:
            flash('Confirm your new password')
            return redirect('/change')
        check = db.execute('SELECT * FROM users WHERE name = ?', name)
        if len(check) == 0:
            flash("Username doesn't exist")
            return redirect('/change')
        if check[0]['name'] != name:
            flash('Wrong Username')
            return redirect('/change')

        if check_password_hash(check[0]['hash'],oldpassword) == False:
            flash('Wrong old password!')
            return redirect('/change')
        if not check_password_pattern(newpassword):
            flash('Please enter a correct new password')
            return redirect('/change')
        if newpassword != newpasswordc:
            flash("Passwords don't match")
            return redirect('/change')
        
        db.execute('UPDATE users SET hash=?,password=? WHERE id=?;',generate_password_hash(newpassword),newpassword,check[0]['id'])
        flash('Password Changed!')
        return redirect('/login')
        
        
    return render_template('changePassword.html')


@app.route('/account',methods=['POST','GET'])
def account():
    information = db.execute('SELECT * FROM users WHERE id = ?',session['user'])
    history = db.execute('SELECT * FROM history WHERE user_id = ?',session['user'])
    if request.method == 'GET':
        return render_template('account.html', information=information , history=history)
    if request.method == 'POST' :
        removal = request.form.get('removal')
        name = request.form.get('name')
        email = request.form.get('ChangeEmail')
        if not name and not email:
           db.execute('DELETE FROM history WHERE user_id = ? AND video_title = ?;',session['user'],removal)
           return redirect('/account')
        
        if not name and not removal:
            email = db.execute('SELECT * FROM users WHERE email = ?', email)
            if len(email) != 0:
                flash('Email Already Taken')
                return redirect('/account')
            db.execute('UPDATE users SET email = ? WHERE id = ?;', email , session['user'])
        else:
            name1 = db.execute('SELECT * FROM users WHERE name = ?', name)
            if len(name1) != 0:
                flash('Username Already Taken')
                return redirect('/account')
            db.execute('UPDATE users SET name = ? WHERE id = ?;',name , session['user'])
            session['name'] = name
        return redirect('/account')
    

