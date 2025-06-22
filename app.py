# Fix the models add location sa acmpaigns table

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text, func, distinct
from extensions import db
from datetime import date
from collections import defaultdict


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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

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
    campaign = Campaigns.query.filter_by(CampaignID=campaign_id).first()

    name = campaign.Name.title()
    urgency = campaign.isUrgent
    date_posted = campaign.DatePosted
    location = campaign.Location
    description = campaign.Description
    organizer_name = campaign.organizer.Name.title()
    status = campaign.Status  # <-- Add this

    # Query campaign item needs
    result = CampaignDetails.query.filter_by(CampaignID=campaign_id).all()

    item_list = list({item.ItemID for item in result})

    # Now prepare a dict: item_id => {name, allocated, needed}
    item_statuses = {}
    for detail in result:
        item_id = detail.ItemID
        item_name = detail.item.ItemName
        needed = detail.QuantityNeeded

        # Get total allocated in inventory (sum of QuantityAvailable)
        allocated = db.session.query(
            func.sum(Inventory.QuantityAvailable)
        ).filter_by(CampaignID=campaign_id, ItemID=item_id).scalar() or 0

        item_statuses[item_id] = {
            'name': item_name,
            'allocated': allocated,
            'needed': needed
        }

    return render_template(
        'donor_campaign_post.html',
        role=session.get('role'),
        name=name,
        urgency=urgency,
        organizer_name=organizer_name,
        description=description,
        date_posted=date_posted,
        location=location,
        item_list=item_list,
        item_statuses=item_statuses,
        status=status  # <-- pass to template
    )

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
                    Status='unallocated',  # or 'unallocated'
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

    try:
        avg_stars = sum_stars / len(stars)
    except:
        avg_stars = 'No ratings yet.'
    

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


@app.route('/donor_track')
def donor_track():
    donor_id = session.get('donor_id')  # make sure this is set on login

    # Query: Get item name, quantity donated, and campaign name (if allocated)
    results = (
        db.session.query(
            Campaigns.Name.label('campaign_name'),
            ItemList.ItemName.label('item_name'),
            func.sum(Inventory.QuantityAvailable).label('quantity')
        )
        .join(Donations, Donations.DonationID == Inventory.DonationID)
        .join(Campaigns, Campaigns.CampaignID == Inventory.CampaignID)
        .join(ItemList, ItemList.ItemID == Inventory.ItemID)
        .filter(Donations.DonorID == donor_id)
        .group_by(Campaigns.Name, ItemList.ItemName)
        .all()
    )

    # Structure: {campaign_name: [(item_name, quantity), ...]}
    campaigns = defaultdict(list)
    for row in results:
        campaigns[row.campaign_name].append((row.item_name, row.quantity))

    return render_template('donor_track.html', campaigns=campaigns, role = session.get('role'))


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
@app.route('/org_campaign')
def org_campaign():
    active_campaigns = Campaigns.query.filter_by(OrganizerID = session.get('organizer_id'), Status = 'Active').all()
    completed_campaigns = Campaigns.query.filter_by(OrganizerID = session.get('organizer_id'), Status = 'Completed').all()
    
    return render_template('organizer_allocate.html', active_campaigns=active_campaigns,\
                     completed_campaigns=completed_campaigns, role=session.get('role'))

@app.route('/org_request_list')
def org_request_list():
    requests = Requests.query.filter_by(OrganizerID=session.get('organizer_id')).all()
    return render_template('organizer_request_list.html', requests = requests, role = session.get('role'))

@app.route('/delete_request')
def delete_request():
    request_id = request.args.get('request_id')
    del_request = Requests.query.filter_by(RequestID=request_id).first()
    db.session.delete(del_request)
    db.session.commit()
    return redirect(url_for('org_request_list'))

@app.route('/org_update_form')
def org_update_form():
    organizer_id = session.get('organizer_id')

    # Get all donations for the organizer
    all_donations = Donations.query.filter_by(OrganizerID=organizer_id).all()

    # Use a dictionary to store unique donors, mapping DonorID to the first found Donation object
    # This ensures only one Donation object per DonorID is kept.
    unique_donations_by_donor = {}
    for donation in all_donations:
        if donation.DonorID not in unique_donations_by_donor:
            unique_donations_by_donor[donation.DonorID] = donation
    
    donations = list(unique_donations_by_donor.values())

    return render_template('organizer_update_form.html', donations=donations, role=session.get('role'))

@app.route('/org_update_form/submit_update', methods = ['POST'])
def submit_update():
    updateText = request.form.get('message')
    organizer_id = session.get('organizer_id')
    donor_id = request.form.get('donor_id')

    db.session.add(Updates(UpdateText=updateText, DonorID = donor_id, OrganizerID=organizer_id))
    db.session.commit()

    return redirect(url_for('org_request_list'))

@app.route('/allocate')
def allocate():
    organizer_id = session.get('organizer_id')
    allocation_results = []

    # Get all campaigns belonging to the logged-in organizer
    campaigns = Campaigns.query.filter_by(OrganizerID=organizer_id).order_by(
        Campaigns.isUrgent.desc(),
        Campaigns.DatePosted.asc()
    ).all()

    print(campaigns)

    for campaign in campaigns:
        campaign_summary = {'name': campaign.Name, 'allocations': []}
        
        campaign_details = CampaignDetails.query.filter_by(CampaignID=campaign.CampaignID).all()

        for detail in campaign_details:
            item_id = detail.ItemID
            print(item_id)
            item_name = detail.item.ItemName
            print(item_name)
            qty_needed = detail.QuantityNeeded
            print(qty_needed)

            # Check how much has already been allocated
            already_allocated = db.session.query(func.sum(Inventory.QuantityAvailable)).filter_by(
                CampaignID=campaign.CampaignID,
                ItemID=item_id,
                Status = 'allocated' # this is my addtion, I think this will help
            ).scalar() or 0

            remaining_needed = qty_needed - already_allocated
            if remaining_needed <= 0:
                continue

            # Get unallocated inventory FROM THIS ORGANIZER only
            inventories = (
                db.session.query(Inventory)
                .join(Donations, Inventory.DonationID == Donations.DonationID)
                .filter(
                    Inventory.ItemID == item_id,
                    Inventory.CampaignID == None,
                    Inventory.Status == 'unallocated',
                    Donations.OrganizerID == organizer_id  # restrict by organizer
                )
                .order_by(Inventory.InventoryID.asc())
                .all()
            )

            total_allocated = 0
            for inv in inventories:
                if remaining_needed <= 0:
                    break

                if inv.QuantityAvailable <= remaining_needed:
                    inv.CampaignID = campaign.CampaignID
                    inv.Status = 'allocated'
                    inv.AllocationDate = date.today()
                    total_allocated += inv.QuantityAvailable
                    remaining_needed -= inv.QuantityAvailable
                else:
                    # Split inventory
                    allocated_qty = remaining_needed
                    excess_qty = inv.QuantityAvailable - remaining_needed

                    inv.QuantityAvailable = allocated_qty
                    inv.CampaignID = campaign.CampaignID
                    inv.Status = 'allocated'
                    inv.AllocationDate = date.today()

                    new_inv = Inventory(
                        DonationID=inv.DonationID,
                        ItemID=inv.ItemID,
                        QuantityAvailable=excess_qty,
                        CampaignID=None,
                        Status='unallocated',
                        AllocationDate=None
                    )
                    db.session.add(new_inv)

                    total_allocated += allocated_qty
                    remaining_needed = 0

            if total_allocated > 0:
                campaign_summary['allocations'].append({
                    'item': item_name,
                    'allocated': total_allocated
                })

        print(campaign_summary)
        # Check if the campaign is now fully allocated
        fully_allocated = True
        for detail in campaign_details:
            allocated = db.session.query(func.sum(Inventory.QuantityAvailable)).filter_by(
                CampaignID=campaign.CampaignID,
                ItemID=detail.ItemID
            ).scalar() or 0

            if allocated < detail.QuantityNeeded:
                fully_allocated = False
                break

        if fully_allocated:
            campaign.Status = "Completed"

        if campaign_summary['allocations']:
            allocation_results.append(campaign_summary)

    print(allocation_results)
    db.session.commit()
    flash("Allocation complete!")
    return render_template('allocation_results.html', results=allocation_results)

@app.route('/post_campaign')
def post_campaign():
    return render_template('organizer_campaign_post_form.html', role=session.get('role'))

@app.route('/post_campaign/submit', methods=['POST'])
def submit_campaign():
    organizer_id = session.get('organizer_id')

    if not organizer_id:
        flash("Organizer not logged in.")
        return redirect(url_for('login'))  

    # Get campaign main fields
    title = request.form.get('title')
    location = request.form.get('location')
    description = request.form.get('description')
    urgency = request.form.get('urgency')  
    is_urgent = 1 if urgency == 'yes' else 0

    # Create campaign
    new_campaign = Campaigns(
        OrganizerID=organizer_id,
        Name=title,
        Description=description,
        Status="Active",
        isUrgent=is_urgent,
        DatePosted=date.today(),
        Location=location
    )
    db.session.add(new_campaign)
    db.session.commit() 

    items = {
        'rice': request.form.get('rice_quantity'),
        'clothes': request.form.get('clothes_quantity'),
        'canned goods': request.form.get('canned_goods_quantity'),
        'medical kits': request.form.get('medical_kits_quantity')
    }

    for item_name, qty in items.items():
        if qty and qty.strip() and int(qty) > 0:
            item_record = ItemList.query.filter(ItemList.ItemName.ilike(item_name)).first()
            if item_record:
                campaign_detail = CampaignDetails(
                    CampaignID=new_campaign.CampaignID,
                    ItemID=item_record.ItemID,
                    QuantityNeeded=int(qty)
                )
                db.session.add(campaign_detail)

    db.session.commit()
    flash("Campaign posted successfully.")
    return redirect(url_for('org_campaign')) 

if __name__ == '__main__':
    app.run(debug=True)

