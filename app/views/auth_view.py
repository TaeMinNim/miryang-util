from flask import Blueprint, request, flash, redirect, url_for, render_template, g, session
from app.forms import Login_Form
from app import db
from app.models import User
from datetime import datetime

import sys

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for('main.index'))
    form = Login_Form()
    if request.method == 'POST':
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if not user:
            id=int(round(datetime.today().timestamp() * 1000))
            user = User(id=id, username=form.username.data, nickname=form.nickname.data)
            db.session.add(user)
            db.session.commit()
            session['id'] = user.id
            return redirect(url_for('main.index'))
        else:
            if user.username == form.username.data:
                session['id'] = user.id
            else:
                flash('닉네임이 중복됩니다')
    return render_template('auth/login_form.html', form=form)

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



