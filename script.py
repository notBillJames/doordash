from datetime import datetime

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


# FIXME
def format_query(dct):
    if dct['destination'] == None:
        query = '''
        INSERT INTO orders VALUES
        
        '''


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
    dct["dropoff_time"] = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
    if dct["destination"] = 
