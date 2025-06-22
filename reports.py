import pandas as pd
from sqlalchemy import create_engine, text

class Report:

    def __init__(self):
        self.engine = create_engine('sqlite:///instance/db.sqlite')
        self.con = self.engine.connect()

    def most_donated(self):
        query = """
        SELECT
          o.OrganizerID,
          o.Name,
          COUNT(d.DonationID) AS donation_count
        FROM Organizers o
        JOIN Donations d ON o.OrganizerID = d.OrganizerID
        GROUP BY o.OrganizerID, o.Name
        ORDER BY donation_count DESC
        LIMIT 5;
        """
        rs = self.con.execute(text(query))
        df = pd.DataFrame(rs.fetchall(), columns=rs.keys())  # include column names
        return df

    def left_available(self, organizer_id):
        query = """
        SELECT
          il.ItemID,
          il.ItemName AS Name,
          COALESCE(SUM(i.QuantityAvailable), 0) AS total_available
        FROM Inventory i
        JOIN ItemList il ON i.ItemID = il.ItemID
        JOIN Campaigns c ON i.CampaignID = c.CampaignID
        WHERE c.OrganizerID = :organizer_id
        GROUP BY il.ItemID, il.ItemName;
        """
        rs = self.con.execute(text(query), {'organizer_id': organizer_id})
        df = pd.DataFrame(rs.fetchall(), columns=rs.keys())
        return df

    def total_donation(self):
        query  = """
        -- Raw SQL
        SELECT
        d.DonorID,
        dr.Name,
        COUNT(d.DonationID)        AS times_donated,
        COALESCE(SUM(dd.Quantity), 0) AS total_items_donated
        FROM Donations d
        JOIN Donors dr
        ON d.DonorID = dr.DonorID
        LEFT JOIN DonationDetails dd
        ON d.DonationID = dd.DonationID
        GROUP BY
        d.DonorID,
        dr.Name;
        """

        rs = self.con.execute(text(query))
        df = pd.DataFrame(rs.fetchall(), columns = rs.keys())
        return df

    def most_requested_items(self):
        query = """
        -- Raw SQL
        SELECT
        rd.ItemID,
        il.ItemName,
        COUNT(*) AS request_count
        FROM RequestDetails rd
        JOIN ItemList il
        ON rd.ItemID = il.ItemID
        GROUP BY
        rd.ItemID,
        il.ItemName
        ORDER BY
        request_count DESC;
        """

        rs = self.con.execute(text(query))
        df = pd.DataFrame(rs.fetchall(), columns = rs.keys())
        return df
    
    def number_campaigns(self, organizer_id):
        query = """
        -- Raw SQL (for a given organizer_id)
        SELECT
        Status,
        COUNT(*) AS count
        FROM Campaigns
        WHERE
        OrganizerID = :organizer_id
        GROUP BY
        Status;
        """
        rs = self.con.execute(text(query), {'organizer_id': organizer_id})
        df = pd.DataFrame(rs.fetchall(), columns = rs.keys())
        return df
    
if __name__ == '__main__':
    pass

