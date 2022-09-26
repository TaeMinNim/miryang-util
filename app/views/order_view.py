from flask import Blueprint, request, g, redirect, url_for
from app.forms import Order_Form, Posting_Form
from datetime import datetime
import wtforms_json
from app import db_connection
import jwt
from config.development import SECRET_KEY

bp = Blueprint('order',__name__, url_prefix='/order')
wtforms_json.init()

def analyze_token():
    try:
        token = request.headers['Authorization']
    except Exception as e:
        return False
    else:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except Exception as e:
            return False
        else:
            g.user_id = decoded_token['id']

@bp.route('/posting', methods=['POST'])
def delivery_posting():
    analyze_token()
    db = db_connection()
    cursor = db.cursor()

    json = request.get_json()
    print(json)
    form = Posting_Form.from_json(json)

    today = datetime.today()
    print(datetime.now())
    id = int(round(today.timestamp() * 1000))
    sql = """
    INSERT INTO DELIVERY_POST (id, user_id, store_id, title, content, order_time, current_member, min_member, min_member, max_member, is_closed
    VALUE({id}, {user_id}, {store_id}, '{title}', '{content}', {order_time}, {current_member}, {min_member}, {max_member}, {is_closed})""".format(
        id=id,
        user_id=g.user_id,
        store_id=form.store_id.data,
        title=form.title.data,
        content=form.content.data,
        order_time=datetime.now(),
        current_member=1,
        min_member=form.min_member.data,
        max_member=form.max_member.data,
        is_closed=0
        )
    cursor.execute(sql)
    db.commit()
    db.close()



@bp.route('/detail/<int:groupID>', methods=('GET', 'POST'))
def detail(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        json = request.get_json()
        for order in json:
            form = Order_Form.from_json(order['formdata'])
            today = datetime.today()
            id = int(round(today.timestamp() * 1000))
        return ('', 204)
