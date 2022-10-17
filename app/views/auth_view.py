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

@bp.route('/overlap/username')
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

@bp.route('/overlap/studentnum')
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

@bp.route('/overlap/nickname')
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
    json = request.get_json()
    form = Signup_Form.from_json(json)
    if request.method == 'POST':
        db = db_connection()
        cursor = db.cursor()
        id = int(round(datetime.today().timestamp() * 1000))

        hashed_pw = bcrypt.hashpw(form.pw.data.encode('utf-8'), bcrypt.gensalt())
        hashed_pw = hashed_pw.decode('utf-8')
        sql = """INSERT INTO SERVICE_USER 
        (id, user_name, pw, student_num, nick_name) VALUE({id}, '{user_name}', '{pw}', {student_num}, '{nick_name}')
        """.format(id=id, user_name=form.user_name.data, pw=hashed_pw, student_num=form.student_num.data, nick_name=form.nick_name.data)

        try:
            cursor.execute(sql)
        except Exception as e:
            result = jsonify(result='false')
        else:
            db.commit()
            result = jsonify(result='true')
        finally:
            db.close()
            return result


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        db = db_connection()
        cursor = db.cursor()
        json = request.get_json()
        form = Login_Form.from_json(json)


        sql = "SELECT id, pw FROM SERVICE_USER WHERE user_name = '{user_name}'".format(user_name=form.user_name.data)
        if cursor.execute(sql):
            data = cursor.fetchall()

            id = data[0][0]
            hashed_pw = data[0][1]
            request_pw = form.pw.data.encode('utf-8')
            compare_pw = bcrypt.checkpw(request_pw, hashed_pw.encode('utf-8'))

            if compare_pw:
                data = {
                    'id' : id
                }
                token = jwt.encode(data, SECRET_KEY)

                response = make_response({'result' : 'true'})
                response.headers['Content-Type'] = 'Application/json'
                response.headers['Authentication'] = 'Bearer {token}'.format(token=token)
            else:
                response = make_response({'result' : 'fasle'})
        else:
            response = make_response({'result' : 'fasle'})
        return response

@bp.before_app_request
def analyze_token():
    try:
        token = request.headers['Authorization']
    except Exception as e:
        g.user_id = None
    else:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except Exception as e:
            return ('Not valid token', 500)
        else:
            g.user_id = decoded_token['id']