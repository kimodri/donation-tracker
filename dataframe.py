from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///db.sqlite')
con = engine.connect()

rs = con.execute("SELECT * FROM Campaigns")

campaigns_df = pd.DataFrame(rs.fetchall())
campaigns_df = rs.keys()

print(campaigns_df)