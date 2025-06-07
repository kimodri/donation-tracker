from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text
from extensions import db

# Create the app instance
app = Flask(__name__)
app.secret_key = 'hello'

# Absolute path for SQLite (reliable path handling)
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure the 'instance' folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
# db.init_app(app)

# import models here
from models import (
    Users,
    Campaigns,
    CampaignRequests,
    Communities,
    Donations,
    DonationDetails,
    Donors,
    Feedbacks,
    Inventory,
    ItemList,
    Organizers,
    Representatives,
    Requests,
    Updates
)


# bind the db instance to app
db.init_app(app)
# Create the tables if they don't exist yet (This will create db.db automatically)
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        print("Received POST request") 
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')
        community = request.form.get('community')
        address = request.form.get('address')

        
        # Add to the users table
        db.session.add(Users(Email = email, Password = password, Role = role))
        
        if role == 'donor':
            db.session.add(Donors(Name = name, Email = email))
            db.session.commit()

        elif role == 'organizer':
            db.session.add(Organizers(Name = name, Email = email))
            db.session.commit()

        else:
            db.session.add(Representatives(Name = name, Email = email))
            db.session.add(Communities(Name = community, Address = address))
            db.session.commit()

        
        # # do flash here pre
        return redirect(url_for('thank_you'))

    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request == 'GET':
        return render_template('login.html')

    # Get the things
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    print(password)


    try:
        # query the user
        result = Users.query.filter_by(Email=email).first()
        print(result.Email)
        print(result.Role)

        if result:
            if result.Password == password: 
                session['user_id'] = result.UserID
                session['email'] = result.Email
                session['role'] = result.Role

                if result.Role == 'donor':
                    return "Donor Page"
                    # return redirect('')  # homepage for donor
                elif result.Role == 'organizer':
                    return "Organizer Page"
                    # return redirect('') # homepage for organizer
                else:
                    return "Representative Page"
                    # return redirect('') # homepage for representative
            else:
                flash('Incorrect password')
                return redirect('/login')

    except AttributeError:
        flash('Account not found')
        # redicrect to sign in page whch will call the sign in function
        return render_template('login.html')


@app.route('/organizer_list', methods = ['GET', 'POST'])
def organizer_list():
    pass
    # render_template()

@app.route('/donate', methods = ['GET', 'POST'])
def donate():
    pass 
    '''
    INSERT INTO Feedbacks()
    if wala pang ganong connection 
    '''

@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    if request == 'GET':
        return render_template('feedback.html')
    else:
        '''
            SELECT Feedback, stars
            FROM feedbacks
            WHERE user = session['user'] AND organizer = organizer
        
        '''
        # kunin kung para kanino, kunin kung sino, kunin yung star, tanggalin siya sa pinag-anuhan
        pass
        # mula sa session na nagawa mo sa login kunn mo yung uder_id, lagay mo sa db

@app.route('/update', methods = ['GET', 'POST'])
def update():
    pass



@app.route('/thank-you')
def thank_you():    
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)

