from flask import Blueprint, render_template, flash, request, session, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Dash, Order, Note
from . import db
from datetime import datetime
import json
import functools

views = Blueprint('views', __name__)


def session_started(view):
    # Wrapper to check if a dashing session has been started
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session['dashStart'] is None:
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


@views.route('/start-dashing', methods=['GET', 'POST'])
@login_required
def start_dashing():
    if request.method == 'POST':
        session['dashLocation'] = request.form.get('location')
        session['dashPromo'] = request.form.get('promo')
        session['dashStart'] = datetime.strftime(
            datetime.now(),
            '%Y-%m-%d %H:%M%S'
        )

        return redirect(url_for('views.log_order'))

    return render_template('start_dashing.html', user=current_user)


@views.route('/log-order', methods=['GET', 'POST'])
@login_required
@session_started
def log_order():
    return render_template('log_order.html', user=current_user)


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
