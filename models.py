# from extensions import db
# from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey, Integer, DateTime, func
# from datetime import date, datetime

# class Users(db.Model):
#     __tablename__ = 'Users'
#     UserID = Column(Integer, primary_key=True, autoincrement=True)
#     Email = Column(String(31))
#     Password = Column(String(20))
#     Role = Column(String(14))

# class Organizers(db.Model):
#     __tablename__ = 'Organizers'
#     OrganizerID = Column(Integer, primary_key=True, autoincrement=True)
#     Name = Column(String(100))
#     Email = Column(String(50))

#     def __repr__(self):
#         return f"<Organizer(OrganizerID='{self.OrganizerID}', Name='{self.Name}')>"

# class Donors(db.Model):
#     __tablename__ = 'Donors'
#     DonorID = Column(Integer, primary_key=True, autoincrement=True)
#     Name = Column(String(100))
#     Email = Column(String(50))

#     def __repr__(self):
#         return f"<Donor(DonorID='{self.DonorID}', Name='{self.Name}')>"

# class Communities(db.Model):
#     __tablename__ = 'Communities'
#     CommunityID = Column(Integer, primary_key=True, autoincrement=True)
#     Name = Column(String(100))
#     Address = Column(Text)

#     def __repr__(self):
#         return f"<Community(CommunityID='{self.CommunityID}', Name='{self.Name}')>"

# class Representatives(db.Model):
#     __tablename__ = 'Representatives'
#     RepresentativeID = Column(Integer, primary_key=True, autoincrement=True)
#     CommunityID = Column(Integer, ForeignKey('Communities.CommunityID'))
#     Name = Column(String(100))
#     Email = Column(String(50))

#     community = db.relationship("Communities", backref="representatives")

#     def __repr__(self):
#         return f"<Representative(RepresentativeID='{self.RepresentativeID}', Name='{self.Name}')>"

# class ItemList(db.Model):
#     __tablename__ = 'ItemList'
#     ItemID = Column(Integer, primary_key=True, autoincrement=True)
#     ItemName = Column(String(100))

#     def __repr__(self):
#         return f"<Item(ItemID='{self.ItemID}', ItemName='{self.ItemName}')>"

# class Campaigns(db.Model):
#     __tablename__ = 'Campaigns'
#     CampaignID = Column(Integer, primary_key=True, autoincrement=True)
#     OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))
#     Name = Column(String(100))
#     Description = Column(Text)
#     Status = Column(String(20))
#     isUrgent = Column(Boolean)
#     DatePosted = Column(Date, default=date.today)
#     Location = Column(String(31))

#     organizer = db.relationship("Organizers", backref="campaigns")

#     def __repr__(self):
#         return f"<Campaign(CampaignID='{self.CampaignID}', Name='{self.Name}')>"

# class CampaignDetails(db.Model):
#     __tablename__ = 'CampaignDetails'
#     CdID = Column(Integer, primary_key=True, autoincrement=True)
#     # RequestID = Column(Integer, ForeignKey('Requests.RequestID'))
#     CampaignID = Column(Integer, ForeignKey('Campaigns.CampaignID'))
#     ItemID = Column(Integer, ForeignKey('ItemLists.ItemID'))
#     QuantityNeeded = Column(Integer)

#     # request = db.relationship("Requests", backref = "campaign_requests")  # something is wrong here
#     campaign = db.relationship("Campaigns", backref="campaign_requests")
#     item = db.relationship("ItemList", backref="campaign_requests")

#     def __repr__(self):
#         return f"<CampaignDetails(CampaignID='{self.CampaignID}', ItemID='{self.ItemID}', QuantityNeeded={self.QuantityNeeded})>"

# class Donations(db.Model):
#     __tablename__ = 'Donations'
#     DonationID = Column(Integer, primary_key=True, autoincrement=True)
#     DonorID = Column(Integer, ForeignKey('Donors.DonorID'))
#     OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))
#     Timestamp = Column(DateTime, default=datetime.now, server_default=func.now())

#     donor = db.relationship("Donors", backref="donations")
#     organizer = db.relationship("Organizers", backref="donations")

#     def __repr__(self):
#         return f"<Donation(DonationID='{self.DonationID}', Timestamp='{self.Timestamp}')>"

# class DonationDetails(db.Model):
#     __tablename__ = 'DonationDetails'
#     DonationDetailID = Column(Integer, primary_key=True, autoincrement=True)
#     DonationID = Column(Integer, ForeignKey('Donations.DonationID'))
#     ItemID = Column(Integer, ForeignKey('ItemLists.ItemID'))
#     Quantity = Column(Integer)

#     donation = db.relationship("Donations", backref="donation_details")
#     item = db.relationship("ItemList", backref="donation_details")

#     def __repr__(self):
#         return f"<DonationDetail(DonationDetailID='{self.DonationDetailID}', Quantity={self.Quantity})>"

# class Inventory(db.Model):
#     __tablename__ = 'Inventory'
#     InventoryID = Column(Integer, primary_key=True, autoincrement=True)
#     DonationDetailID = Column(Integer, ForeignKey('DonationDetails.DonationDetailID'))
#     ItemID = Column(Integer, ForeignKey('ItemLists.ItemID'))
#     QuantityAvailable = Column(Integer)
#     CampaignID = Column(Integer, ForeignKey('Campaigns.CampaignID'))
#     Timestamp = Column(DateTime)
#     Status = Column(String(20))
#     AllocationDate = Column(DateTime, nullable=True)

#     donation_detail = db.relationship("DonationDetails", backref="inventories")
#     item = db.relationship("ItemList", backref="inventories")
#     campaign = db.relationship("Campaigns", backref="inventories")

#     def __repr__(self):
#         return f"<Inventory(InventoryID='{self.InventoryID}', Status='{self.Status}')>"

# class Feedbacks(db.Model):
#     __tablename__ = 'Feedbacks'
#     FeedbackID = Column(Integer, primary_key=True, autoincrement=True)
#     Comment = Column(Text)
#     Stars = Column(Integer)
#     DonorID = Column(Integer, ForeignKey('Donors.DonorID'))
#     OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))

#     donor = db.relationship("Donors", backref="feedbacks")
#     organizer = db.relationship("Organizers", backref="feedbacks")

#     def __repr__(self):
#         return (f"<Feedback(FeedbackID='{self.FeedbackID}', Stars={self.Stars}, "
#                 f"DonorID='{self.DonorID}', OrganizerID='{self.OrganizerID}')>")

# class Requests(db.Model):
#     __tablename__ = 'Requests'
#     RequestID = Column(Integer, primary_key=True, autoincrement=True)
#     OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))
#     RepresentativeID = Column(Integer, ForeignKey('Representatives.RepresentativeID'))
#     Message = Column(Text)

#     organizer = db.relationship("Organizers", backref="requests")
#     representative = db.relationship("Representatives", backref="requests")

#     def __repr__(self):
#         return f"<Request(RequestID='{self.RequestID}', Message='{self.Message[:20]}...')>"

# class RequestDetails(db.Model):
#     __tablename__ = 'RequestDetails'
#     rdID = Column(Integer, primary_key = True, autoincrement=True)
#     RequestID = Column(Integer, ForeignKey('Requests.RequestID'))
#     ItemID = Column(Integer, ForeignKey('ItemLists.ItemID'))
#     QuantityNeeded = Column(Integer)

#     request = db.relationship("Requests", backref='requestdetails')
#     item = db.relationship("ItemList", backref='requestdetails')

# class Updates(db.Model):
#     __tablename__ = 'Updates'
#     UpdateID = Column(Integer, primary_key=True, autoincrement=True)
#     UpdateText = Column(Text)
#     DonorID = Column(Integer, ForeignKey('Donors.DonorID'))
#     OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))

#     donor = db.relationship("Donors", backref="updates")
#     organizer = db.relationship("Organizers", backref="updates")

#     def __repr__(self):
#         return f"<Update(UpdateID='{self.UpdateID}', UpdateText='{self.UpdateText[:20]}...')>"



from extensions import db
from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey, Integer, DateTime, func
from datetime import date, datetime

class Users(db.Model):
    __tablename__ = 'Users'
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(31))
    Password = Column(String(20))
    Role = Column(String(14))

class Organizers(db.Model):
    __tablename__ = 'Organizers'
    OrganizerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Email = Column(String(50))

    def __repr__(self):
        return f"<Organizer(OrganizerID='{self.OrganizerID}', Name='{self.Name}')>"

class Donors(db.Model):
    __tablename__ = 'Donors'
    DonorID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Email = Column(String(50))

    def __repr__(self):
        return f"<Donor(DonorID='{self.DonorID}', Name='{self.Name}')>"

class Communities(db.Model):
    __tablename__ = 'Communities'
    CommunityID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Address = Column(Text)

    def __repr__(self):
        return f"<Community(CommunityID='{self.CommunityID}', Name='{self.Name}')>"

class Representatives(db.Model):
    __tablename__ = 'Representatives'
    RepresentativeID = Column(Integer, primary_key=True, autoincrement=True)
    CommunityID = Column(Integer, ForeignKey('Communities.CommunityID'))
    Name = Column(String(100))
    Email = Column(String(50))

    community = db.relationship("Communities", backref="representatives")

    def __repr__(self):
        return f"<Representative(RepresentativeID='{self.RepresentativeID}', Name='{self.Name}')>"

class ItemList(db.Model):
    __tablename__ = 'ItemList'
    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    ItemName = Column(String(100))

    def __repr__(self):
        return f"<Item(ItemID='{self.ItemID}', ItemName='{self.ItemName}')>"

class Campaigns(db.Model):
    __tablename__ = 'Campaigns'
    CampaignID = Column(Integer, primary_key=True, autoincrement=True)
    OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))
    Name = Column(String(100))
    Description = Column(Text)
    Status = Column(String(20))
    isUrgent = Column(Integer)
    DatePosted = Column(Date, default=date.today)
    Location = Column(String(31))

    organizer = db.relationship("Organizers", backref="campaigns")

    def __repr__(self):
        return f"<Campaign(CampaignID='{self.CampaignID}', Name='{self.Name}')>"

class CampaignDetails(db.Model):
    __tablename__ = 'CampaignDetails'
    CdID = Column(Integer, primary_key=True, autoincrement=True)
    CampaignID = Column(Integer, ForeignKey('Campaigns.CampaignID'))
    ItemID = Column(Integer, ForeignKey('ItemList.ItemID'))
    QuantityNeeded = Column(Integer)

    campaign = db.relationship("Campaigns", backref="campaign_requests")
    item = db.relationship("ItemList", backref="campaign_requests")

    def __repr__(self):
        return f"<CampaignDetails(CampaignID='{self.CampaignID}', ItemID='{self.ItemID}', QuantityNeeded={self.QuantityNeeded})>"

class Donations(db.Model):
    __tablename__ = 'Donations'
    DonationID = Column(Integer, primary_key=True, autoincrement=True)
    DonorID = Column(Integer, ForeignKey('Donors.DonorID'))
    OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))
    Date = Column(Date, default=date.today, server_default=func.now())

    donor = db.relationship("Donors", backref="donations")
    organizer = db.relationship("Organizers", backref="donations")

    def __repr__(self):
        return f"<Donation(DonationID='{self.DonationID}', Date='{self.Date}')>"

class DonationDetails(db.Model):
    __tablename__ = 'DonationDetails'
    DonationDetailID = Column(Integer, primary_key=True, autoincrement=True)
    DonationID = Column(Integer, ForeignKey('Donations.DonationID'))
    ItemID = Column(Integer, ForeignKey('ItemList.ItemID'))
    Quantity = Column(Integer)

    donation = db.relationship("Donations", backref="donation_details")
    item = db.relationship("ItemList", backref="donation_details")

    def __repr__(self):
        return f"<DonationDetail(DonationDetailID='{self.DonationDetailID}', Quantity={self.Quantity})>"

class Inventory(db.Model):
    __tablename__ = 'Inventory'
    InventoryID = Column(Integer, primary_key=True, autoincrement=True)
    DonationID = Column(Integer, ForeignKey('Donations.DonationID'))  # Rename field properly

    ItemID = Column(Integer, ForeignKey('ItemList.ItemID'))
    QuantityAvailable = Column(Integer)
    CampaignID = Column(Integer, ForeignKey('Campaigns.CampaignID'), nullable = True)
    Status = Column(String(20))
    AllocationDate = Column(Date, default=date.today, server_default=func.now(), nullable=True)

    item = db.relationship("ItemList", backref="inventories")
    campaign = db.relationship("Campaigns", backref="inventories")
    donation = db.relationship("Donations", backref="inventories")  # Match to Donations, not DonationDetails

    def __repr__(self):
        return f"<Inventory(InventoryID='{self.InventoryID}', Status='{self.Status}')>"

class Feedbacks(db.Model):
    __tablename__ = 'Feedbacks'
    FeedbackID = Column(Integer, primary_key=True, autoincrement=True)
    Comment = Column(Text)
    Stars = Column(Integer)
    DonorID = Column(Integer, ForeignKey('Donors.DonorID'))
    OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))

    donor = db.relationship("Donors", backref="feedbacks")
    organizer = db.relationship("Organizers", backref="feedbacks")

    def __repr__(self):
        return (f"<Feedback(FeedbackID='{self.FeedbackID}', Stars={self.Stars}, "
                f"DonorID='{self.DonorID}', OrganizerID='{self.OrganizerID}')>")

class Requests(db.Model):
    __tablename__ = 'Requests'
    RequestID = Column(Integer, primary_key=True, autoincrement=True)
    OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))
    RepresentativeID = Column(Integer, ForeignKey('Representatives.RepresentativeID'))
    Message = Column(Text)

    organizer = db.relationship("Organizers", backref="requests")
    representative = db.relationship("Representatives", backref="requests")
    requestdetails = db.relationship("RequestDetails", back_populates="request", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Request(RequestID='{self.RequestID}', Message='{self.Message[:20]}...')>"

class RequestDetails(db.Model):
    __tablename__ = 'RequestDetails'
    rdID = Column(Integer, primary_key=True, autoincrement=True)
    RequestID = Column(Integer, ForeignKey('Requests.RequestID'))
    ItemID = Column(Integer, ForeignKey('ItemList.ItemID'))
    QuantityNeeded = Column(Integer)

    request = db.relationship("Requests", back_populates="requestdetails")
    item = db.relationship("ItemList", backref="requestdetails")

class Updates(db.Model):
    __tablename__ = 'Updates'
    UpdateID = Column(Integer, primary_key=True, autoincrement=True)
    UpdateText = Column(Text)
    DonorID = Column(Integer, ForeignKey('Donors.DonorID'))
    OrganizerID = Column(Integer, ForeignKey('Organizers.OrganizerID'))

    donor = db.relationship("Donors", backref="updates")
    organizer = db.relationship("Organizers", backref="updates")

    def __repr__(self):
        return f"<Update(UpdateID='{self.UpdateID}', UpdateText='{self.UpdateText[:20]}...')>"
