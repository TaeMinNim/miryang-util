from flask import Blueprint, request, flash, redirect, url_for, render_template, g, session, jsonify
from app.forms import Signup_Form
from datetime import datetime
import pymysql

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/username-overlap-check/')
def usernameOverlapCheck():
    username = request.args['user_name']
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234',db='delivery', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE username = '{username}'".format(username=username)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = Signup_Form()
    if request.method == 'POST':
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='DELIVERY', charset='utf8')
        cursor = db.cursor()
        id = int(round(datetime.today().timestamp() * 1000))
        print(id, form.username.data, form.pw.data, form.email.data, form.nickname.data)
        print(type(id), type(form.username.data), type(form.pw.data), type(form.email.data), type(form.nickname.data))
        sql = 'INSERT INTO SERVICE_USER (id, username, pw, email, nickname) VALUE({id}, \'{username}\', \'{pw}\', \'{email}\', \'{nickname}\')'.format(id=id, username=form.username.data, pw=form.pw.data, email=form.email.data, nickname=form.nickname.data)
        cursor.execute(sql)
        db.commit()
        db.close()

    else:
        return render_template('auth/signup_form.html', form=form)




