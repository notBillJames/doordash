from datetime import datetime
import sqlalchemy as sql
import pandas as pd


def time_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return now


# Dash class creates and stores order information, then commits it to db
class Dash:
    def __init__(self) -> None:
        self.start = datetime.now()
        self.orders = {
            "restaurant": [],
            "destination": [],
            "distance": [],
            "accept_time": [],
            "pickup_time": [],
            "dropoff_time": []
        }

    # Function to record initial order information
    def start_order(self):
        for key in list(self.orders.keys())[:3]:
            self.orders[key].append(input(f"{key.title()}: "))
        self.orders["accept_time"].append(time_now())

    # Function to record pickup time of order
    def pickup_order(self):
        self.orders["pickup_time"].append(time_now())

    # Function to record dropoff time of order and commit data to table
    def dropoff_order(self):
        self.orders['dropoff_time'].append(time_now())

    def commit_orders(self):
        df = pd.DataFrame.from_dict(self.orders, orient='columns')
        e = sql.create_engine("sqlite:///doordash.db")
        with e.connect() as conn:
            df.to_sql('orders', con=conn, if_exists='append', index=False)
