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


# start_order returns dict with all order data other than dropoff time
def start_order():
    dct = {}
    dct["restaurant"] = input("Restaurant :")
    a = input("Destination :")
    if a == "":
        dct["destination"] = None
    else:
        dct["destination"] = a
    dct["distance"] = int(input("Distance :"))
    dct["pickup_time"] = datetime.now().strftime("%d:%m:%Y %H:%M.%S")
    return dct


def close_order():
    pass
