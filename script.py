from datetime import datetime
import sqlalchemy as sql
import pandas as pd

"""
Information that could be in a DoorDash order:
    1. Restaurant
    2. Distance
    3. Direction
    4. Pay
    5. Tip?
    6. Pickup Time
    7. Dropoff Time
"""


# start_order returns dict with all order data other than dropoff time
def start_order():
    dct = {}
    dct["restaurant"] = input("Restaurant :").title()
    a = input("Destination :")
    if a == "":
        dct["destination"] = None
    else:
        dct["destination"] = a.title()
    dct["distance"] = float(input("Distance :"))
    dct["accept_time"] = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
    return dct


# Function to record pickup time of order
def pickup_order(dct):
    dct["pickup_time"] = datetime.now().strftime("%d/%m/%Y %H:%M.%S")


# Function to record dropoff time of order and commit data to table
def close_order(dct, con):
    dct['dropoff_time'] = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
    df = pd.DataFrame.from_dict(dct, orient='columns')
    e = sql.create_engine("sqlite://doordash.db")
    with e.connect() as conn:
        df.to_sql('orders', conn)
