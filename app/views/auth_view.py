from flask import Blueprint, request, flash, redirect, url_for, render_template, g, session
from app.forms import Login_Form
from app import db
from app.models import User
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for('main.index'))

    form = Login_Form()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if not user:
            id=int(round(datetime.today().timestamp() * 1000))
            user = User(id=id, username=form.username.data, nickname=form.nickname.data)
            db.session.add(user)
            db.session.commit()
            session['nickname'] = user.nickname
            return redirect(url_for('main.index'))
        else:
           flash('닉네임이 중복됩니다')
    return render_template('auth/login_form.html', form=form)

@bp.route('/logout/')
def logout():
    if not g.user:
        return redirect(url_for('main.index'))
    nickname = session['nickname']
    user = User.query.filter_by(nickname=nickname).first()
    db.session.delete(user)
    db.session.commit()
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request
def login_required():
    nickname = session.get('nickname')
    if nickname is None:
        g.user = None
    else:
        g.user = User.query.filter_by(nickname=nickname).first()



