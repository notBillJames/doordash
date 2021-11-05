from datetime import datetime
import sqlalchemy as sql
import pandas as pd


def time_now():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return now


# Dash class creates and stores order information, then commits it to db
class Dash:
    def __init__(self, conn="sqlite:///doordash.db") -> None:
        self.conn = conn
        self.commit = False
        self.dash_info = {
            'start': [time_now()],
            'location': [input('Where are you dashing? ').lower()],
            'promo': [int(input('Enter any promo '))]
        }
        self.orders = {
            'restaurant': [],
            'destination': [],
            'distance': [],
            'pay': [],
            'accept_time': [],
            'pickup_time': [],
            'dropoff_time': []
        }

    # Function to record initial order information
    def start_order(self):
        self.orders['accept_time'].append(time_now())
        for key in list(self.orders.keys())[:2]:
            self.orders[key].append(input(f'{key.title()}: '))
        for key in list(self.orders.keys())[2:4]:
            try:
                self.orders[key].append(float(input(f'{key.title()}: ')))
            except ValueError:
                print(f'{key.title()} needs to be a float')

    # Function to record pickup time of order
    def pickup_order(self):
        self.orders['pickup_time'].append(time_now())

    # Function to record dropoff time of order and commit data to table
    def dropoff_order(self):
        self.orders['dropoff_time'].append(time_now())

    def commit_orders(self):
        orders = pd.DataFrame.from_dict(self.orders, orient='columns')
        e = sql.create_engine(self.conn)
        with e.connect() as db:
            orders.to_sql('orders', con=db, if_exists='append', index=False)

        self.orders = {
            'restaurant': [],
            'destination': [],
            'distance': [],
            'pay': [],
            'accept_time': [],
            'pickup_time': [],
            'dropoff_time': []
        }

    def commit_dashes(self):
        self.dash_info['total_pay'] = sum(self.orders['pay'])
        self.dash_info['gas_cost'] = float(input('Gas Cost: '))
        dashes = pd.DataFrame.from_dict(self.dash_info, orient='columns')
        e = sql.create_engine(self.conn)
        with e.connect() as db:
            dashes.to_sql('dashes', con=db, if_exists='append', index=False)
