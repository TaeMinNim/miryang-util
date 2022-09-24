from flask import Blueprint, request, jsonify, make_response
from wtforms_json import from_json
from app.forms import Signup_Form,Login_Form
from datetime import datetime
from config.development import SECRET_KEY
import pymysql
import bcrypt
import jwt
import wtforms_json

wtforms_json.init()
bp = Blueprint('auth', __name__, url_prefix='/auth')

def db_connection():
    db = pymysql.connect(host='localhost', port=3306, user='dbuser', passwd='!miryangUTIL2022',db='UTILITY_SERVICE', charset='utf8')
    return db

@bp.route('/username-overlap-check')
def usernameOverlapCheck():
    user_name = request.args['user_name']
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE user_name = '{user_name}'".format(user_name=user_name)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/studentnum-overlap-check')
def studentnumOverlapCheck():
    student_num = request.args['student_num']
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE student_num = {student_num}".format(student_num=student_num)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/nickname-overlap-check')
def nicknameOverlapCheck():
    nick_name = request.args['nick_name']
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE nick_name = '{nick_name}'".format(nick_name=nick_name)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        return jsonify(response=False)
    else:
        return jsonify(response=True)

@bp.route('/signup', methods=['POST'])
def signup():
    print('request')
    json = request.get_json()
    print(json)
    form = Signup_Form.from_json(json)
    print('form check')
    if request.method == 'POST':
        print('if')
        db = db_connection()
        print('db connect')
        cursor = db.cursor()
        print('cursor success')
        id = int(round(datetime.today().timestamp() * 1000))

        hashed_pw = bcrypt.hashpw(form.pw.data.encode('utf-8'), bcrypt.gensalt())
        hashed_pw = hashed_pw.decode('utf-8')
        print('pw hashed')
        sql = """INSERT INTO SERVICE_USER 
        (id, user_name, pw, student_num, nick_name) VALUE({id}, '{user_name}', '{pw}', {student_num}, '{nick_name}')
        """.format(id=id, user_name=form.user_name.data, pw=hashed_pw, student_num=form.student_num.data, nick_name=form.nick_name.data)
        print(sql)
        cursor.execute(sql)
        print('data insert')
        db.commit()
        print('db commit')
        db.close()
        print('db close')
        return jsonify(result='true')

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        db = db_connection()
        cursor = db.cursor()
        form = Login_Form()
        print(form.user_name.data)
        print(form.pw.data)
        sql = "SELECT id, pw FROM SERVICE_USER WHERE user_name = '{user_name}'".format(user_name=form.user_name.data)
        cursor.execute(sql)

        data = cursor.fetchall()
        id = data[0][0]
        hashed_pw = data[0][1]
        request_pw = form.pw.data.encode('utf-8')
        result=bcrypt.checkpw(request_pw, hashed_pw.encode('utf-8'))

        if result:
            data = {
                'id' : id
            }
            token = jwt.encode(data, SECRET_KEY)

            response = make_response({'result' : 'true'})
            response.headers['Content-Type'] = 'Application/json'
            response.headers['Authentication'] = 'Bearer {token}'.format(token=token)
            return response
        else:
            return '로그인 실패'


