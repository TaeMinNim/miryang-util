from flask import Blueprint, request, flash, redirect, url_for, render_template, g, session, jsonify
from app.forms import Signup_Form
from datetime import datetime
import pymysql

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/username-overlap-check/')
def usernameOverlapCheck():
    username = request.args['user_name']
    db = pymysql.connect(host='localhost', port=3306, user='dbuser', passwd='!miryangUTIL2022',db='UTILITY_SERVICE', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE username = '{username}'".format(username=username)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/studentnum-overlap-check/')
def studentnumOverlapCheck():
    studentnum = request.args['student_num']
    db = pymysql.connect(host='localhost', port=3306, user='dbuser', passwd='!miryangUTIL2022', db='UTILITY_SERVICE', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE student_num = {studentnum}".format(studentnum=studentnum)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/nickname-overlap-check/')
def nicknameOverlapCheck():
    nickname = request.args['nickname']
    db = pymysql.connect(host='localhost', port=3306, user='dbuser', passwd='!miryangUTIL2022', db='UTILITY_SERVICE', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE nickname = '{nickname}'".format(nickname=nickname)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/signup/', methods=['POST'])
def signup():
    form = Signup_Form()
    if request.method == 'POST':
        db = pymysql.connect(host='localhost', port=3306, user='dbuser', passwd='!miryangUTIL2022', db='UTILITY_SERVICE', charset='utf8')
        cursor = db.cursor()
        id = int(round(datetime.today().timestamp() * 1000))
        print(id, form.username.data, form.pw.data, form.student_num.data, form.nickname.data)
        print(type(form.student_num.data))
        sql = """INSERT INTO SERVICE_USER 
        (id, username, pw, student_num, nickname) VALUE({id}, '{username}', '{pw}', {student_num}, '{nickname}')
        """.format(id=id, username=form.username.data, pw=form.pw.data, student_num=form.student_num.data, nickname=form.nickname.data)
        print(sql)
        cursor.execute(sql)
        db.commit()
        db.close()
        return ('성공')




