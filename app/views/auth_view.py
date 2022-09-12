from flask import Blueprint, request, flash, redirect, url_for, render_template, g, session
from app.forms import Signup_Form
from app import db
from app.models import User
from datetime import datetime

import sys

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = Signup_Form()
    if request.method == 'POST':
        id = int(round(datetime.today().timestamp() * 1000))
        user = User(id=id,
                    username=form.username.data,
                    nickname=form.nickname.data,
                    userID=form.id.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/signup_form.html', form=form)
@bp.route('/logout/')
def logout():
    if not g.user:
        return redirect(url_for('main.index'))
    id = session['id']
    '''user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()'''
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request
def login_required():
    id = session.get('id')
    if id is None:
        g.user = None
    else:
        g.user = User.query.get(id)



