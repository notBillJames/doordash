from typing import _promote
from flask import Blueprint, render_template, flash, request, session, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Dashes, Orders, Note, PendingOrders
from . import db
from sqlalchemy.sql import func
import json
import functools

views = Blueprint('views', __name__)


def dash_started(view):
    # Wrapper to check if a dashing session has been started
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'dashID' not in session:
            flash(
                'Start a Dash Session before Logging Orders',
                category='error'
            )
            return redirect(url_for('views.dash'))

        return view(*args, **kwargs)

    return wrapped_view


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(
                data=note,
                user_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template('home.html', user=current_user)


@views.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    if request.method == 'POST':
        if request.form.get('startDash'):
            dashLocation = request.form.get('location')
            dashPromo = request.form.get('promo')

            dash = Dashes(
                start=func.now(),
                location=dashLocation,
                promo=dashPromo,
                user_id=current_user.id
            )
            db.session.add(dash)
            db.session.commit()

            user_dashes = Dashes.query.filter_by(user_id=current_user.id)
            current_dash = user_dashes.order_by(Dashes.start.desc())
            session['dashID'] = current_dash.first().id
            session['dashStage'] = 'dashing'
            session['orderStage'] = 'accept'

            return redirect(url_for('views.dash'))
        if request.form.get('endDashing'):
            current_dash = Dashes.query.filter_by(id=session['dashID']).first()
            current_dash.end = func.now()

            db.session.commit()
            session['dashID'] = 'ending'

            return redirect(url_for('views.dash'))
        if request.form.get('commitDashing'):
            current_dash = Dashes.query.filter_by(id=session['dashID']).first()
            orders = current_dash.orders
            current_dash.end = func.now()
            current_dash.total_pay = orders.query(func.sum(orders.pay))
            current_dash.gas_cost = request.form.get('gas_cost')
            current_dash.total_miles = request.form.get('total_miles')

            db.session.commit()

            return redirect(url_for('views.dash'))

    if 'dashID' not in session:
        # on dashID means session has not been started,
        # stage should be "starting"
        return render_template(
            'dash.html',
            user=current_user,
            stage='starting'
        )
    elif session['dashStage'] == 'dashing':
        # FIXME
        # add information to display with
        current_dash = Dashes.query.filter_by(id=session['dashID']).first()
        orders = current_dash.orders
        location = f'Location: {current_dash.location.title()}'
        start = f'Start Time: {current_dash.start.strftime("%I:%M %p")}'
        promo = f'Promo: ${current_dash.promo}/order'
        pay_gross = orders.query(func.sum(orders.pay))
        pay = f'Pay this session: ${pay_gross}'
        strings = [location, start, promo, pay]
        return render_template(
            'dash.html',
            user=current_user,
            stage='dashing',
            strings=strings
        )
    elif session['dashStage'] == 'ending':
        # FIXME
        # should have info strings and add forms to finish dash
        current_dash = Dashes.query.filter_by(id=session['dashID']).first()
        
        return render_template(
            'dash.html',
            user=current_user,
            stage='ending',
            strings=strings
        )
    

@views.route('/order', methods=['GET', 'POST'])
@login_required
@dash_started
def order():
    if request.method == 'POST':
        if request.form.get('orderReceive'):
            restaurant = request.form.get('restaurant')
            destination = request.form.get('destination')
            distance = request.form.get('distance')
            pay = request.form.get('pay')
            order = PendingOrders(
                restaurant=restaurant,
                destination=destination,
                distance=distance,
                pay=pay,
                accept_time=func.now(),
                user_id=current_user.id,
                dash_id=session['dashID']
            )

            db.session.add(order)
            db.session.commit()

            obj = PendingOrders.query.filter_by(user_id=current_user.id)
            session['orderID'] = obj.first().id
            session['orderStage'] = 'pickup'

            return redirect(url_for('views.order'))

        elif request.form.get('orderPickup'):
            order = PendingOrders.query.filter_by(id=session['orderID']).first()
            order.pickup_time = func.now()
            db.session.commit()

            session['orderStage'] = 'deliver'

            return redirect(url_for('views.order'))
        elif request.form.get('orderDeliver'):
            order = PendingOrders.query.filter_by(id=session['orderID']).first()
            new_order = Orders(
                restaurant=order.restaurant,
                destination=order.destination,
                distance=order.distance,
                pay=order.distance,
                accept_time=order.accept_time,
                pickup_time=order.pickup_time,
                dropoff_time=func.now(),
                user_id=current_user.id,
                dash_id=session['dashID']
            )

            db.session.add(new_order)
            db.session.delete(order)
            db.session.commit()

            session['orderStage'] = 'accept'

            session.pop('orderID', None)
            return redirect(url_for('views.order'))
    if session['orderStage'] == 'accept':
        return render_template(
            'order.html',
            user=current_user,
            stage=session['orderStage']
        )
    elif session['orderStage'] == 'pickup':
        obj = PendingOrders.query.filter_by(user_id=current_user.id).first()
        restaurant = f'Restaurant: {obj.restaurant}'
        destination = f'Destination: {obj.destination}'
        distance = f'Distance: {obj.distance}'
        pay = f'Pay: ${obj.pay}'
        accept_time = f'Accept Time: {obj.accept_time.strftime("%I:%M %p")}'
        strings = [
            restaurant,
            destination,
            distance,
            pay,
            accept_time
        ]

        return render_template(
            'order.html',
            user=current_user,
            stage=session['orderStage'],
            strings=strings
        )
    elif session['orderStage'] == 'deliver':
        obj = PendingOrders.query.filter_by(user_id=current_user.id).first()
        restaurant = f'Restaurant: {obj.restaurant}'
        destination = f'Destination: {obj.destination}'
        distance = f'Distance: {obj.distance}'
        pay = f'Pay: ${obj.pay}'
        accept_time = f'Accept Time: {obj.accept_time.strftime("%I:%M %p")}'
        pickup_time = f'Pickup Time: {obj.pickup_time.strftime("%I:%M %p")}'
        strings = [
            restaurant,
            destination,
            distance,
            pay,
            accept_time,
            pickup_time
        ]

        return render_template(
            'order.html',
            user=current_user,
            stage=session['orderStage'],
            strings=strings
        )


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
