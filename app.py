from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# configurations:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doneate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# databases:
db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    role = db.Column(db.String(14))




# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Adding sa table
        db.session.add(Users(username = username, password = password, role = role))
        db.session.commit()
        # do flash here pre
        return render_template('signin.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request == 'GET':
        return render_template('login.html')

    else:
        # Get the things
        username = request.form.get('username')
        password = request.form.get('password')

        # query the user
        user = Users.query.filter_by(username=username).first()

        if user:
            if user.password == password: 
                session['user_id'] = user.user_id
                session['username'] = user.username
                session['role'] = user.role

                if user.role == 'donor':
                    return redirect('')  # homepage for donor
                elif user.role == 'organizer':
                    return redirect('') # homepage for organizer
                else:
                    return redirect('') # homepage for representative
            else:
                flash('Incorrect password')

        else:
            flash('Username not found')
            # redicrect to sign in page whch will call the sign in function

        return redirect('/login')


@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    if request == 'GET':
        return render_template('feedback.html')
    else:
        # kunin kung para kanino, kunin kung sino, kunin yung star, tanggalin siya sa pinag-anuhan
        pass
        # mula sa session na nagawa mo sa login kunn mo yung uder_id, lagay mo sa db


@app.route('/thank-you')
def thank_you():    
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)

