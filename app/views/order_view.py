from flask import Blueprint, request, g, make_response, jsonify
from app.forms import Posting_Form
from datetime import datetime
import wtforms_json
import json
from bson import ObjectId
from pymongo import ReturnDocument


from app import mongodb_connection

bp = Blueprint('order',__name__, url_prefix='/order')
wtforms_json.init()

#가게 조회 관련

#201
@bp.route('/store/list')
def inquire_delivery_store_list():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['delivery']

    projection = {
        'menu': False
    }
    store_list = db.delivery_store.find({}, projection)

    json_store_list = []
    for store in store_list:
        store_json={
            'store_id': str(store['_id']),
            'store_name': store['store_name'],
            'min_order': store['min_order'],
            'fee': store['fee']
        }
        json_store_list.append(store_json)

    return make_response(json.dumps(json_store_list, ensure_ascii=False))

#202
@bp.route('/menu/list')
def inquire_delivery_menu_list():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['delivery']

    store_id = request.args['store_id']

    find={
        '_id': ObjectId(store_id)
    }
    project={
        '_id': False,
        'menus.section_name': True,
        'menus.menu_name': True,
        'menus.menu_price': True
    }
    menu_list = db.delivery_store.find_one(find, project)['menus']
    json_menu_list = []

    #Dictionary 형태로 section_name, index를 key:value 형태로 저장
    section_index = {}
    for menu in menu_list:
        if menu['section_name'] in section_index:
            index = section_index[menu['section_name']]
            menu_json = {
                'menu_name': menu['menu_name'],
                'menu_price': menu['menu_price']
            }
            json_menu_list[index]['menus'].append(menu_json)

        else:
            section_menu_json = {
                'section_name': menu['section_name'],
                'menus': [{
                    'menu_name': menu['menu_name'],
                    'menu_price': menu['menu_price']
                }]
            }
            json_menu_list.append(section_menu_json)
            section_index[menu['section_name']] = len(json_menu_list) - 1

    return make_response(json.dumps(json_menu_list, ensure_ascii=False))

#203
@bp.route('/menu/detail')
def inquire_delivery_menu_detail():
    if not g.user_id:
        return ('access denied', 500)
    client = mongodb_connection()
    db = client['delivery']

    store_id = request.args['store_id']
    menu_name = request.args['menu_name']

    find = {
        '_id': ObjectId(store_id),
    }
    projection = {
        'menus': {
            '$elemMatch': {'menu_name': menu_name}
        }
    }
    menu_detail = db.delivery_store.find_one(find, projection)['menus'][0]['groups']
    return make_response(json.dumps(menu_detail, ensure_ascii=False))

#게시글 관련
#204
@bp.route('/post/posting', methods=['POST'])
def post_delivery_posting():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    mongo_db = client['delivery']

    post = request.get_json()
    form = Posting_Form.from_json(post)

    find = {'_id': ObjectId(form.store_id.data)}
    projection = {'menus': False}
    store = mongo_db.delivery_store.find_one(find, projection)

    today = datetime.now()
    data = {
        'user_id': g.user_id,
        'join_users': [g.user_id],
        'nick_name': g.nick_name,
        'store': store,
        'title': form.title.data,
        'content': form.content.data,
        'place': form.place.data,
        'order_time': form.order_time.data,
        'min_member': form.min_member.data,
        'max_member': form.max_member.data,
        'update_date': today.strftime('%Y-%m-%dT%H:%M:%S'),
        'views': 0,
        'is_closed': False,
        'user_orders': []
    }

    try:
        _id = mongo_db.delivery_post.insert_one(data)
    except Exception as e:
        print(e)
        success = False
    else:
        post_id = str(_id.inserted_id)
        success = True

    return jsonify(post_id=post_id, success=success)

#205
@bp.route('/post/detail/<string:post_id>')
def inquire_delivery_post_detail(post_id):
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['delivery']

    find = {
        '_id': ObjectId(post_id)
    }
    update = {
        '$inc': { 'views': 1 }
    }

    try:
        post = db.delivery_post.find_one_and_update(find, update, return_document=ReturnDocument.AFTER)
    except Exception as e:
        print(e)
        success = False
    else:
        success = True

    post['_id'] = str(post['_id'])
    post['store']['_id'] = str(post['store']['_id'])

    return make_response(json.dumps(post, ensure_ascii=False))


#206
@bp.route('/post/update', methods=['GET', 'PATCH'])
def update_delivery_post():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['delivery']
    if request.method == 'GET':
        post_id = request.args['post_id']

        find = {
            '_id': ObjectId(post_id)
        }
        projection = {
            '_id': False,
            'title': True,
            'content': True,
            'order_time': True,
            'place': True,
            'min_member': True,
            'max_member': True
        }
        post = db.delivery_post.find_one(find, projection)

        return make_response(json.dumps(post, ensure_ascii=False))

    update_data = request.get_json()
    post_id = update_data['post_id']
    find = {
        '_id': ObjectId(post_id)
    }
    update={
        '$set': {
            'title': update_data['title'],
            'content': update_data['content'],
            'order_time': update_data['order_time'],
            'place': update_data['place'],
            'min_member': update_data['min_member'],
            'max_member': update_data['max_member']
        }
    }
    try:
        db.delivery_post.update_one(find, update)
    except Exception as e:
        print(e)
        success = False
    else:
        success = True
    return jsonify(post_id=post_id, success=success)

#207
@bp.route('/post/isClosed/condition-switch', methods=['PATCH'])
def delivery_post_condition_switch():
    json = request.get_json()
    post_id = json['post_id']

    client = mongodb_connection()
    db = client['delivery']

    find = {
        '_id': ObjectId(post_id)
    }
    post = db.delivery_post.find_one(find)

    update = {
        '$set': { 'is_closed' : not post['is_closed'] }
    }
    try:
        db.delivery_post.update_one(find, update)
    except Exception as e:
        print(e)
        success = False
    else:
        success = True

    return jsonify(post_id=post_id, success=success, is_closed= not post['is_closed'])

#211
@bp.route('/post/join/condition-switch', methods=['PATCH'])
def delivery_post_join():
    if not g.user_id:
        return ('access denied', 500)
    client = mongodb_connection()
    db = client['delivery']
    json = request.get_json()
    post_id = json['post_id']
    find = {
        '_id': ObjectId(post_id)
    }
    post = db.delivery_post.find_one(find)

    if g.user_id == post['user_id']:
        success = False
        return ('대표자는 그룹을 탈퇴할 수 없습니다', 500)

    if g.user_id in post['join_users']:
        join = False
        success = True
        update = {
            '$pull': {
                'join_users': g.user_id,
                'user_orders': {'user_id': g.user_id}
            }
        }
    else:
        join = True
        success = True
        update = {
            '$push': {
                'join_users': g.user_id
            }
        }
    try:
        db.delivery_post.update_one(find, update)
    except Exception as e:
        print(e)
        success = False
    else:
        success = True
    return jsonify(post_id=post_id, success=success, join=join)

#213
@bp.route('/post/list')
def delivery_post_list():
    if not g.user_id:
        return ('access denied', 500)
    client = mongodb_connection()
    db = client['delivery']

    projection = {
        'content': False,
        'user_orders': False
    }
    post_list = list(db.delivery_post.find({}, projection))
    for post in post_list:
        post['_id'] = str(post['_id'])
        post['store']['_id'] = str(post['store']['_id'])
    return make_response(json.dumps(post_list, ensure_ascii=False))


#주문하기 관련

#209
@bp.route('/ordering', methods=['POST'])
def delivery_ordering():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['delivery']

    order_json = request.get_json()
    post_id = order_json['post_id']
    store_id = order_json['store_id']
    orders = order_json['orders']

    orders = price(orders, db, store_id)

    user_order = {
        'user_id': g.user_id,
        'nick_name': g.nick_name,
        'orders': orders
    }

    find = {
        '_id': ObjectId(post_id)
    }

    update = {
        '$push': { 'user_orders': user_order }
    }
    db.delivery_post.update_one(find, update)

    return jsonify(post_id=post_id, success=True)

#210
@bp.route('/ordering/update', methods=['GET', 'PATCH'])
def delivery_ordering_update():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['delivery']

    if request.method == 'GET':
        post_id = request.args['post_id']
        find = {
            '_id': ObjectId(post_id)
        }
        projection = {
            'user_orders': {
                '$elemMatch': {'user_id': g.user_id}
            }
        }
        user_order = db.delivery_post.find_one(find, projection)
        print(user_order)
        user_order = user_order['user_orders'][0]
        return make_response(json.dumps(user_order, ensure_ascii=False))

    update_json = request.get_json()
    post_id = update_json['post_id']
    store_id = update_json['store_id']
    orders = update_json['orders']

    orders = price(orders , db, store_id)

    find = {
        '_id': ObjectId(post_id),
        'user_orders': {
            '$elemMatch': {
                'user_id': g.user_id
            }
        }
    }

    update = {
        '$set': { 'user_orders.$.orders': orders }
    }

    db.delivery_post.update_one(find, update)

    return jsonify(post_id=post_id, success=True)


def price(orders, db, store_id):
    find = {"_id": ObjectId(store_id)}
    menu_list = db.delivery_store_find_one(find)['menus']

    def find_option_in_group(group, option_id):
        for option in group['options']:
            if option['option_id'] == option_id:
                return option

    def find_group_in_menu(menu, group_id):
        for group in menu['groups']:
            if group_id == group['group_id']:
                return group

    def find_menu(menu_name):
        for menu in menu_list:
            if menu['menu_name'] == menu_name:
                return menu

    sum_price = 0
    for order_menu in orders:
        menu = find_menu(order_menu['menu_name'])

        order_menu['menu_price'] = menu['menu_price']
        sum_price += order_menu['menu_price']
        if len(menu['groups']) > 0:
            for order_group in order_menu['groups']:
                group = find_group_in_menu(menu, order_group['group_id'])
                for order_option in order_group['options']:
                    option = find_option_in_group(group, order_option)

                    order_group['options'].remove(order_option)
                    order_group['options'].append(option)

                    sum_price += option['option_price']
        order_menu['sum_price'] = sum_price
    return orders