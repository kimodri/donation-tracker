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
                    
                    donors = [i.Email for i in Users.query.filter_by(Role = 'donor')]
                    id = donors.index(session['email']) + 1
                    session['donor_id'] = id
                    print(type(session['donor_id']))
                    return "Donor Page"
                    # return redirect('')  # homepage for donor
                elif result.Role == 'organizer':
                    organizers = [i.Email for i in Users.query.filter_by(Role = 'organizer')]
                    id = organizers.index(session['email']) + 1
                    session['organizer_id'] = id
                    return "Organizer Page"
                    # return redirect('') # homepage for organizer
                else:
                    representatives = [i.Email for i in Users.query.filter_by(Role = 'representative')]
                    id = representatives.index(session['email']) + 1
                    session['representative_id'] = id
                    return "Representative Page"
                    # return redirect('') # homepage for representative
            else:
                flash('Incorrect password')
                return redirect('/login')

    except AttributeError:
        print(result.Email)
        print(result.Password)
        flash('Account not found')
        # redicrect to sign in page whch will call the sign in function
        return render_template('login.html')

@app.route('/organizerList', methods = ['GET', 'POST'])
def organizerList():

    # This functionlity is for the users whose role is a donor
    if session['role'] == 'donor':
        # returns list of organizerID
        # Get all donations by the donor
        result = Donations.query.filter_by(DonorID=session['donor_id']).all()

        # Use the relationship to access organizer names
        organizer_names = list({donation.organizer.Name for donation in result})

        dummy_organizers = ['Kim', 'Triselle', 'Matan','Audrey', 'John', 'Julliane']
        return render_template('donor_organizer.html', organizers = dummy_organizers, role = session['role'])
    
    elif session['role'] == 'representative':
        result = Organizers.query.all()
        organizer_names = [i.Name for i in result]

        dummy_organizer_names = ['ABS-CBN', 'GMA', 'Rastaman Inc']
        render_template('rep_request_org.html', organizer_names = dummy_organizer_names, role = session['role'])
    
    else:
        return "You are not allowed to visit this URL."


# @app.route('/sendRequest', methods = ['GET', 'POST'])
# def sendRequest():
#     if request == 'GET':
#         if session['role'] == 'representative':
#             organizer = request.args.get('organizer')
#             render_template('rep_request_form.html', role = session['role'], organizer=organizer)
#         else:
#             return "You are not allowed to visit this URL."
   
   
#     else:
#         organizerName = request.form.get('organizer')
#         result = Organizers.query.filter_by(Name = organizerName)
#         organizer_id = result.OrganizerID

#         message = request.form.get('message')
#         representative_id = session.get('representative_id')

#         # db.session.add(Requests(organizer_id, session['reprsentative_id']), message)

#         # items = request.form.get('cb') # returns a list

#         # quantities = [request.form.get(i) for i in ['rnum', 'cnum', 'cgnum', 'mednum'] if request.form.get(i) != None]

#         # n = len(items)
#         # for i in range(n):
#         #     db.session.add(CampaignRequests(organizer_id), )
#         # Map ItemID to quantity input name
        
#         item_quantity_map = {
#             '1': 'rnum',     # Rice
#             '2': 'cnum',     # Clothes
#             '3': 'cgnum',    # Canned Goods
#             '4': 'mednum'    # Medical Kits
#         }

#         # Create and commit the Request first
#         new_request = Requests(
#             OrganizerID=organizer_id,
#             RepresentativeID=representative_id,
#             Message=message
#         )
#         db.session.add(new_request)
#         db.session.commit()

#         # Ang paglalagay ng campaignrequest ay kapag meron ng campaign
#         request_id = new_request.RequestID

#         # Get selected checkboxes (ItemIDs)
#         selected_items = request.form.getlist('cb')

#         for item_id in selected_items:
#             quantity_input_name = item_quantity_map.get(item_id)
#             if quantity_input_name:
#                 quantity = request.form.get(quantity_input_name)
#                 if quantity:
#                     campaign_id = ... # Retrieve or decide how to determine CampaignID
#                     new_cr = CampaignRequests(
#                         RequestID=request_id,
#                         CampaignID=campaign_id,
#                         ItemID=item_id,
#                         QuantityNeeded=int(quantity)
#                     )
#                     db.session.add(new_cr)

#         db.session.commit()


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
        if session['role'] == 'organizer':
            result = Feedbacks.query.filter_by(OrganizerID = session.get('organizer_id'))
            
            names = result.DonorID # join the names
            
            comments = result.Comment 
            stars = result.Stars
            starSum = 0
            for star in stars:
                starSum += star
            avgStars = starSum / len(stars)

            return render_template('feedbacks.html', role = session['role'], avgStars = avgStars, \
                                   names = names, comments=comments)
        

        elif session['role'] == 'representative':
            organizerName = request.args.get('name')
            result = Feedbacks.query.filter_by(Name=organizerName)
            comments = result.Comment

            render_template('feedbacks.html', role = session.get('role'), name = organizerName, \
                            message = comments)



    else:
        # I want to get the organizerID
        donor_id = session.get('donor_id')
        message = request.form.get('message')
        rating = int(request.form.get('rating'))


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
    return render_template('thankyou.html', role = session['role'])

if __name__ == '__main__':
    app.run(debug=True)

