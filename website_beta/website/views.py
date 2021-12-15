from flask import Blueprint, render_template, flash, request, session, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Dash, Order, Note, PendingOrder
from . import db
from datetime import datetime
from sqlalchemy.sql import func
import json
import functools

views = Blueprint('views', __name__)


def session_started(view):
    # Wrapper to check if a dashing session has been started
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session['dashStart'] is None:
            flash('Start a Dash Session before ordering', category='error')
            return redirect(url_for('views.start_dashing'))

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
def start_dashing():
    if request.method == 'POST':
        dashLocation = request.form.get('location')
        dashPromo = request.form.get('promo')

        dash = Dash(
            start=func.now(),
            location=dashLocation,
            promo=dashPromo
        )
        db.session.add(dash)
        db.session.commit()

        session['dashID'] = Dash.query.order_by(Dash.start.desc()).first().id

        return redirect(url_for('views.log_order'))

    return render_template('start_dashing.html', user=current_user)


@views.route('/order', methods=['GET', 'POST'])
@login_required
@session_started
def log_order():
    if request.method == 'POST':
        if request.form['orderReceive']:
            restaurant = request.form.get('restaurant')
            destination = request.form.get('destination')
            distance = request.form.get('distance')
            pay = request.form.get('pay')
            order = PendingOrder(
                restaurant=restaurant,
                destination=destination,
                distance=distance,
                pay=pay,
                accept_time=func.now()
            )

            db.session.add(order)
            db.session.commit()

            obj = PendingOrder.query.order_by(Dash.start.desc()).first()
            session['orderID'] = obj.id

            return redirect(url_for('views.pickup_order'))

    return render_template('log_order.html', user=current_user)


'''
@views.route('/pickup-order', methods=['GET', 'POST'])
@login_required
@session_started
def pickup_order():
    return render_template('pickup_order.html')
'''


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
