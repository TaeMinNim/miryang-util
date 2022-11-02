import pymysql.err
from flask import Blueprint, request, jsonify, make_response, g
from app.forms import Signup_Form,Login_Form
from datetime import datetime
from config.development import SECRET_KEY
from app import db_connection
import bcrypt
import jwt
import wtforms_json

wtforms_json.init()
bp = Blueprint('auth', __name__, url_prefix='/auth')

#100
@bp.route('/check/overlap/username')
def check_username_overlap():
    user_name = request.args['user_name']
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE user_name = '{user_name}'".format(user_name=user_name)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        isOverlapped = False
    else:
        isOverlapped = True

    return jsonify(isOverlapped=isOverlapped)

#101
@bp.route('/check/overlap/studentnum')
def check_overlap_studentnum():
    student_num = request.args['student_num']
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE student_num = {student_num}".format(student_num=student_num)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        isOverlapped = False
    else:
        isOverlapped = True

    return jsonify(isOverlapped=isOverlapped)

#102
@bp.route('/check/overlap/nickname')
def check_overlap_nickname():
    nick_name = request.args['nick_name']
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT id FROM SERVICE_USER WHERE nick_name = '{nick_name}'".format(nick_name=nick_name)
    user = cursor.execute(sql)
    db.close()
    if user == 0:
        isOverlapped = False
    else:
        isOverlapped = True

    return jsonify(isOverlapped=isOverlapped)

#103
@bp.route('/signup', methods=['POST'])
def signup():
    json = request.get_json()
    form = Signup_Form.from_json(json)
    if request.method == 'POST':
        db = db_connection()
        cursor = db.cursor()
        id = int(round(datetime.today().timestamp() * 1000))

        hashed_pw = bcrypt.hashpw(form.pw.data.encode('utf-8'), bcrypt.gensalt())
        hashed_pw = hashed_pw.decode('utf-8')
        sql = """INSERT INTO SERVICE_USER 
        (id, user_name, pw, nick_name) VALUE({id}, '{user_name}', '{pw}', '{nick_name}')
        """.format(id=id, user_name=form.user_name.data, pw=hashed_pw, student_num=form.student_num.data, nick_name=form.nick_name.data)

        try:
            cursor.execute(sql)
        except pymysql.err.IntegrityError as e:
            print(e)
            success = False
        except Exception as e:
            print(e)
            success = False
        else:
            db.commit()
            success = True
        finally:
            db.close()
            return jsonify(success=success)

#104
@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        db = db_connection()
        cursor = db.cursor()
        json = request.get_json()
        form = Login_Form.from_json(json)

        sql = "SELECT id, nick_name, pw FROM SERVICE_USER WHERE user_name = '{user_name}'".format(user_name=form.user_name.data)
        if cursor.execute(sql):
            data = cursor.fetchall()[0]
            id, nick_name, hashed_pw = data
            request_pw = form.pw.data.encode('utf-8')

            decode_result = bcrypt.checkpw(request_pw, hashed_pw.encode('utf-8'))

            if decode_result:
                data = {
                    'id' : id,
                    'nick_name': nick_name
                }
                token = jwt.encode(data, SECRET_KEY)

                response = make_response({'result' : True, 'user_id': id, 'nick_name': nick_name})
                response.headers['Content-Type'] = 'Application/json'
                response.headers['Authentication'] = '{token}'.format(token=token)
            else:
                response = make_response({'result' : False})
        else:
            response = make_response({'result' : False})

        return response

@bp.before_app_request
def analyze_token():
    try:
        token = request.headers['Authorization']
    except KeyError as e:
        g.user_id = None
    except Exception as e:
        print(e)
    else:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except jwt.exceptions.DecodeError as e:
            return ('Not valid token', 500)
        else:
            g.user_id = decoded_token['id']
            g.nick_name = decoded_token['nick_name']