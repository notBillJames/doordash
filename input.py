from datetime import datetime
import sqlalchemy as sql
import pandas as pd


def time_now():
    now = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
    return now


class Dash:
    def __init__(self) -> None:
        self.start = datetime.now()
        self.orders = []


class Order:
    def __init__(self) -> None:
        self.order_info = {
            "restaurant": [],
            "destination": [],
            "distance": [],
            "accept_time": [],
            "pickup_time": [],
            "dropoff_time": []
        }

    def start_order(self):
        for key in list(self.order_info.keys())[:3]:
            self.order_info[key].append(input(f"{key}: "))
        self.order_info["accept_time"].append(time_now())

    # Function to record pickup time of order
    def pickup_order(self):
        self.order_info["pickup_time"].append(time_now())

    # Function to record dropoff time of order and commit data to table
    def close_order(self):
        self.order_info['dropoff_time'].append(time_now())
        df = pd.DataFrame.from_dict(self.order_info, orient='columns')
        e = sql.create_engine("sqlite://")
        with e.connect() as conn:
            df.to_sql('order_info', con=conn, if_exists='replace', index=False)
