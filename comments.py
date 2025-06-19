# @app.route('/submit_request_form', methods = ['POST'])
# def submit_request_form():
#     organizer_id = request.form.get('organizer')
#     representative_id = session.get('representative_id')
#     message = request.form.get('message') 

#     db.session.add(Requests(OrganizerID=organizer_id, RepresentativeID=representative_id,\
#                             Message=message))
    
#     # but i feel like we should also record kung ilan yung requested
#     db.session.commit()

# @app.route('/donate_form/submit_donate_form', methods = ['POST'])
# def submit_donate_form():
#     organizer_id = request.form.get('organizer_id')
#     rice_quantity = request.form.get('rice-quantity')
#     clothes_quantity = request.form.get('clothes-quantity')
#     canned_goods_quantity = request.form.get('canned-goods-quantity')
#     medical_kits_quantity = request.form.get('medical-kits-quantity')

#     # add to database
#     # donation table    
#     db.session.add(Donations(DonorID = session.get('donor_id'), OrganizerID = organizer_id))
#     db.session.commit()

#     # donation details table
#     donation = Donations.query.filter_by(DonorID=session.get('donor_id')).order_by(Donations.DonationID.desc()).first()

#     items_quantity = [rice_quantity, clothes_quantity, canned_goods_quantity, medical_kits_quantity]
    
#     for idx, qty in enumerate(items_quantity, start=1):  # idx: 1 to 4
#         if qty != 0:
#             db.session.add(DonationDetails(DonationID=donation.DonationID, ItemID=idx, Quantity=qty))
#     db.session.commit()

#     # Add again for inventory
#     donation_detail_id = Donations.query.filter_by(DonorID=session.get('donor_id')).order_by(Donations.DonationID.desc()).first()

#     # Perhaps flash here, thanking
#     return redirect(url_for('donor_donate'))

# @app.route('/organizerList', methods = ['GET', 'POST'])
# def organizerList():
#     # This functionlity is for the users whose role is a donor
#     if session['role'] == 'donor':
#         # returns list of organizerID
#         # Get all donations by the donor
#         result = Donations.query.filter_by(DonorID=session['donor_id']).all()

#         # Use the relationship to access organizer names
#         organizer_names = list({donation.organizer.Name for donation in result})

#         dummy_organizers = ['Kim', 'Triselle', 'Matan','Audrey', 'John', 'Julliane']
#         return render_template('donor_organizer.html', organizers = dummy_organizers, role = session['role'])
    
#     elif session['role'] == 'representative':
#         result = Organizers.query.all()
#         organizer_names = [i.Name for i in result]

#         dummy_organizer_names = ['ABS-CBN', 'GMA', 'Rastaman Inc']
#         render_template('rep_request_org.html', organizer_names = dummy_organizer_names, role = session['role'])
    
#     else:
#         return "You are not allowed to visit this URL."



# @app.route('/feedback', methods = ['GET', 'POST'])
# def feedback():
#     pass

    # if request == 'GET':
    #     if session['role'] == 'organizer':
    #         result = Feedbacks.query.filter_by(OrganizerID = session.get('organizer_id'))
            
    #         names = result.DonorID # join the names
            
    #         comments = result.Comment 
    #         stars = result.Stars
    #         starSum = 0
    #         for star in stars:
    #             starSum += star
    #         avgStars = starSum / len(stars)

    #         return render_template('feedbacks.html', role = session['role'], avgStars = avgStars, \
    #                                names = names, comments=comments)
        

    #     elif session['role'] == 'representative':
    #         organizerName = request.args.get('name')
    #         result = Feedbacks.query.filter_by(Name=organizerName)
    #         comments = result.Comment

    #         render_template('feedbacks.html', role = session.get('role'), name = organizerName, \
    #                         message = comments)



    # else:
    #     # I want to get the organizerID
    #     donor_id = session.get('donor_id')
    #     message = request.form.get('message')
    #     rating = int(request.form.get('rating'))


    #     '''
    #         SELECT Feedback, stars
    #         FROM feedbacks
    #         WHERE user = session['user'] AND organizer = organizer
        
    #     '''
    #     # kunin kung para kanino, kunin kung sino, kunin yung star, tanggalin siya sa pinag-anuhan
    #     pass
    #     # mula sa session na nagawa mo sa login kunn mo yung uder_id, lagay mo sa db























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