# Fix the models add location sa acmpaigns table

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
    CampaignDetails,
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
    RequestDetails,
    Updates
)


# bind the db instance to app
db.init_app(app)
# Create the tables if they don't exist yet (This will create db.db automatically)
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html', role = session.get('role'))


@app.route('/home')
def home():
    return render_template('about_us.html', role = session.get('role'))

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

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    print(request)
    if request.method == 'GET':
        return render_template('login.html')

    # Get the things
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)



        
        try:
            # query the user
            result = Users.query.filter_by(Email=email).first()
            if result == None:
                raise AttributeError("Something went wrong intentionally!")
            # print(result.Email)
            # print(result.Role)

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
                        return redirect(url_for('donor_donate'))
                        # return redirect('')  # homepage for donor
                    elif result.Role == 'organizer':
                        organizers = [i.Email for i in Users.query.filter_by(Role = 'organizer')]
                        id = organizers.index(session['email']) + 1
                        session['organizer_id'] = id
                        return redirect(url_for('org_request_list'))
                        # return redirect('') # homepage for organizer
                    else:
                        representatives = [i.Email for i in Users.query.filter_by(Role = 'representative')]
                        id = representatives.index(session['email']) + 1
                        session['representative_id'] = id
                        return redirect(url_for('rep_request_org'))
                        # return redirect('') # homepage for representative
                else:
                    flash('Incorrect password')
                    return render_template('login.html')

        except AttributeError:
            # print(result.Email)
            # print(result.Password)
            flash('Account not found')
            # redicrect to sign in page whch will call the sign in function
            return render_template('login.html')


# For donors templates
@app.route('/campaign')
def campaign():
    # get the campaign id
    campaign_id = request.args.get('campaign_id')

    # from the id, query the info
    campaign = Campaigns.query.filter_by(CampaignID = campaign_id).all()[0]

    name = campaign.Name.title()

    urgency = campaign.isUrgent

    date_posted = campaign.DatePosted

    location = campaign.Location

    description = campaign.Description

    organizer_name = campaign.organizer.Name.title()

    # Go to campaign request
    result = CampaignDetails.query.filter_by(CampaignID = campaign_id).all()
    item_list = list({item.ItemID for item in result})

    return render_template('donor_campaign_post.html', role = session.get('role'), name=name,\
                           urgency=urgency, organizer_name=organizer_name, description=description,\
                            date_posted=date_posted, location=location, item_list=item_list)


@app.route('/donate_form')
def donate_form():
    # query for the lists of organizers
    result = Organizers.query.all()
    print(result)
    return render_template('donor_donate_form.html', organizers = result, role = session.get('role'))

@app.route('/donate_form/submit_donate_form', methods=['POST'])
def submit_donate_form():
    def parse_quantity(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    organizer_id = request.form.get('organizer_id')
    donor_id = session.get('donor_id')

    rice_quantity = parse_quantity(request.form.get('rice-quantity'))
    clothes_quantity = parse_quantity(request.form.get('clothes-quantity'))
    canned_goods_quantity = parse_quantity(request.form.get('canned-goods-quantity'))
    medical_kits_quantity = parse_quantity(request.form.get('medical-kits-quantity'))

    # Step 1: Insert into Donations table
    donation = Donations(DonorID=donor_id, OrganizerID=organizer_id)
    db.session.add(donation)
    db.session.commit()  # Needed to get donation.DonationID

    # Step 2: Prepare and insert DonationDetails and Inventory
    item_map = {
        "Rice": rice_quantity,
        "Clothes": clothes_quantity,
        "Canned Goods": canned_goods_quantity,
        "Medical Kits": medical_kits_quantity
    }

    for item_name, qty in item_map.items():
        if qty > 0:
            item = ItemList.query.filter_by(ItemName=item_name).first()
            if item:
                # Insert into DonationDetails
                donation_detail = DonationDetails(
                    DonationID=donation.DonationID,
                    ItemID=item.ItemID,
                    Quantity=qty
                )
                db.session.add(donation_detail)

                # Insert into Inventory
                inventory_entry = Inventory(
                    DonationID=donation.DonationID,
                    ItemID=item.ItemID,
                    QuantityAvailable=qty,
                    CampaignID=None,  # No campaign allocated yet
                    Status='available',  # or 'unallocated'
                    AllocationDate=None  # still unallocated
                )
                db.session.add(inventory_entry)

    db.session.commit()

    # Optional: flash a thank-you message
    # flash('Thank you for your donation!', 'success')

    return redirect(url_for('donor_donate'))


@app.route('/donor_donate')
def donor_donate():
    organizers = Organizers.query.all()
    return render_template('donor_donate.html', organizers = organizers, role = session.get('role'))


@app.route('/donor_org_profile')
def donor_org_profile():
    
    # get the organizerID
    organizer_id = int(request.args.get('organizer_id'))

    # get the profile
    organizer = Organizers.query.filter_by(OrganizerID=organizer_id).first()

    # print(organizer)
    # print(organizer.OrganizerID)
    # print(type(organizer.OrganizerID))
    # print(type(organizer))

    stars = Feedbacks.query.filter_by(OrganizerID = organizer_id).all()

    
    sum_stars = 0

    for star in stars:
        sum_stars += star.Stars

    avg_stars = sum_stars / len(stars)
    

    # get the active campaigns by querying and filtering using the id
    active_campaigns = Campaigns.query.filter_by(OrganizerID=organizer_id, Status = 'Active').all() # , Status='Active'

    print(active_campaigns)

    # get the completed campaigns by querying and filtering using the id
    completed_campaigns = Campaigns.query.filter_by(OrganizerID=organizer_id, Status='Completed').all()

    print(completed_campaigns)
    # get the feedback by querying and filtering using the id

    feedbacks = Feedbacks.query.filter_by(OrganizerID=organizer_id).all()

    return render_template('donor_org_profile.html', role = session.get('role'), organizer=organizer.Name.title(), \
                           active_campaigns=active_campaigns, completed_campaigns=completed_campaigns,\
                            feedbacks=feedbacks, avg_stars=avg_stars) 


@app.route('/donor_feedback')
def donor_feedback():

    # get the organizers that the session[role.id] has donated, pass the list 
    donor_id = session.get("donor_id")

    print(donor_id)
    # Get all donations made by the donor
    donations = Donations.query.filter_by(DonorID=donor_id).all()

    print(donations)
    # Get all feedbacks the donor has already submitted

    feedbacks = Feedbacks.query.filter_by(DonorID=donor_id).all()
    print(feedbacks)

    # Get a set of OrganizerIDs that have already been feedbacked
    feedbacked_organizer_ids = {feedback.OrganizerID for feedback in feedbacks}
    print(f"Have already feedbacked on: {feedbacked_organizer_ids}")

    # Filter only the donations to organizers that have NOT been feedbacked
    donations_to_unfeedbacked_organizers = [
        donation for donation in donations if donation.OrganizerID not in feedbacked_organizer_ids
    ]

    # Now extract unique organizer names (in order of appearance)
    from collections import OrderedDict

    organizers = list(OrderedDict.fromkeys(
        donation for donation in donations_to_unfeedbacked_organizers
    ))
    
    # from taas nakuha mo yung listahan ng donations na may OrganizerID
    unfeedbacked_organizers_id = [ i.OrganizerID for i in organizers]

    # organizer_names = list(OrderedDict.fromkeys(
    #     donation.organizer.Name for donation in donations_to_unfeedbacked_organizers
    # ))
    
    print(donor_id)
    print(organizers)
    print(f'unfeedbacked organizers id {unfeedbacked_organizers_id}')

    return render_template('donor_feedback.html', role = session.get('role'), organizers = organizers)

    # return render_template('donor_feedback.html', role = session.get('role'), organizers = organizer_names)

    # preserving the "you can still have an organizer in th elist even if nafeedbackan mo na"
    # donations = Donations.query.filter_by(DonorID=donor_id).all()
    # organizer_names = list({donation.organizer.Name for donation in donations})


# kapag clinick yung feedback button sa overlay ito yung icacall
@app.route('/donor_feedback/submit_feedback', methods = ['POST'])
def donor_submit_feedback():
    def parse_quantity(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
        
    organizer_id = parse_quantity(request.form.get('organizer_id')) # make this an ID
    rating = parse_quantity(request.form.get('rating'))
    comment = request.form.get('message')
    donor_id = session.get('donor_id')

    # add to database
    db.session.add(Feedbacks(Comment=comment, Stars=rating, DonorID=donor_id, OrganizerID=organizer_id))
    db.session.commit()
    return redirect(url_for('donor_feedback'))

@app.route('/donor_update')
def donor_update():
    # since id lang meron sa updatestable kailangan mo magJOIN, ask chatgpt
    updates = Updates.query.filter_by(DonorID = session.get('donor_id')).all()
    return render_template('donor_update.html', role = session.get('role'), updates=updates)


# FOR REPRESENTATIVES

@app.route('/submit_request_form', methods=['POST'])
def submit_request_form():
    from sqlalchemy.exc import SQLAlchemyError

    organizer_id = request.form.get('organizer')
    representative_id = session.get('representative_id')
    message = request.form.get('message')

    try:
        # Step 1: Add request to Requests table
        new_request = Requests(
            OrganizerID=organizer_id,
            RepresentativeID=representative_id,
            Message=message
        )
        db.session.add(new_request)
        db.session.commit()

        # Step 2: Get the inserted RequestID
        request_id = new_request.RequestID

        # Step 3: Map checkbox values to quantity field names
        item_map = {
            "1": "rnum",
            "2": "cnum",
            "3": "cgnum",
            "4": "mednum"
        }

        # Get selected checkboxes (returns a list of values as strings)
        checked_items = request.form.getlist('cb')

        for item_id in checked_items:
            qty_str = request.form.get(item_map.get(item_id))
            try:
                quantity = int(qty_str)
                if quantity > 0:
                    db.session.add(RequestDetails(
                        RequestID=request_id,
                        ItemID=int(item_id),
                        QuantityNeeded=quantity
                    ))
            except (ValueError, TypeError):
                continue  # Skip invalid input

        db.session.commit()
        # flash('Request submitted successfully!', 'success')
        return redirect(url_for('rep_request_org'))

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {e}")
        # flash('Something went wrong while submitting the request.', 'error')
        return redirect(url_for('rep_request_org'))
    
@app.route('/rep_request_org')
def rep_request_org():
    organizers = Organizers.query.all()
    return render_template('rep_request_org.html', organizers = organizers, role = session.get('role'))    

@app.route('/rep_request_org/request_form')
def request_form():
    organizer_id = request.args.get('organizer_id')
    return render_template('rep_request_form.html', organizer_id=organizer_id, role = session.get('role'))

# FOR ORGANIZERS
@app.route('/org_request_list')
def org_request_list():
    requests = Requests.query.filter_by(OrganizerID=session.get('organizer_id')).all()
    return render_template('organizer_request_list.html', requests = requests)

@app.route('/delete_request')
def delete_request():
    request_id = request.args.get('request_id')
    # delete the row with the request
    del_request = Requests.query.filter_by(RequestID = request_id).first()
    db.session.delete(del_request)
    db.session.commit()

@app.route('/org_update_form')
def org_update_form():
    # query those who only donated to you
    donations = Donations.query.filter_by(OrganizerID = session.get('donor_id')).all()
    return render_template('organizer_request_form.html', donations=donations)

@app.route('/org_update_form/submit_update', methods = ['POST'])
def submit_update():
    updateText = request.form.get('message')
    organizer_id = session.get('organizer_id')
    donor_id = request.form.get('donor_id')

    db.session.add(Updates(UpdateText=updateText, DonorID = donor_id, OrganizerID=organizer_id))
    db.session.commit()

@app.route('/allocate')
def allocate():
    pass


@app.route('/donate', methods = ['GET', 'POST'])
def donate():
    pass 
    '''
    INSERT INTO Feedbacks()
    if wala pang ganong connection 
    '''


@app.route('/update', methods = ['GET', 'POST'])
def update():
    pass

@app.route('/thank-you')
def thank_you():    
    return render_template('thankyou.html', role = session['role'])

if __name__ == '__main__':
    app.run(debug=True)

