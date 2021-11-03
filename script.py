from datetime import datetime
import sqlalchemy as sql
import pandas as pd


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

        # Keys needed for Nominatim's geocode()
        self.geopy_dict_keys = ["street", "city", "state", "country",
                                "postalcode"]

    def start_order(self):
        for val in ["restaurant", "destination"]:
            for key in self.geopy_dict_keys:
                self.order_info[val][key] = input(f"{val.title()} {key}")
        self.order_info["distance"].append(float(input("Distance :")))
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
        self.order_info["accept_time"].append(time_now)

    # Function to record pickup time of order
    def pickup_order(self):
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
        self.order_info["pickup_time"].append(time_now)

    # Function to record dropoff time of order and commit data to table
    def close_order(self):
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
        self.order_info['dropoff_time'].append(time_now)
        df = pd.DataFrame.from_dict(self.order_info, orient='columns')
        e = sql.create_engine("sqlite://doordash.db")
        with e.connect() as conn:
            df.to_sql('order_info', con=conn, if_exists='replace', index=False)


"""
DROP TABLE orders;
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    restaurant TEXT DEFAULT NULL,
    destination TEXT DEFAULT NULL,
    distance REAL DEFAULT NULL,
    accept_time TEXT DEFAULT NULL,
    pickup_time TEXT DEFAULT NULL,
    dropoff_time TEXT DEFAULT NULL
);
"""
