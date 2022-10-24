from flask import Blueprint, request, g, make_response, jsonify
from app.forms import Posting_Form
from datetime import datetime
import wtforms_json
import json
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

from app import db_connection

bp = Blueprint('order',__name__, url_prefix='/order')
wtforms_json.init()

#가게 조회 관련

#201
@bp.route('/store/list')
def delivery_store_list():
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    projection={
        'menu': False
    }
    store_list = db.delivery_store.find({}, projection)

    json_list = []
    for store in store_list:
        store_json={
            'store_id': str(store['_id']),
            'store_name': store['store_name'],
            'min_order': store['min_order'],
            'fee': store['fee']
        }
        json_list.append(store_json)

    return make_response(json.dumps(json_list, ensure_ascii=False))

#202
@bp.route('/menu/list')
def delivery_menu_list():
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
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
    json_list = []

    #Dictionary 형태로 section_name, index를 key:value 형태로 저장
    section_index = {}
    for menu in menu_list:
        print(menu)
        if menu['section_name'] in section_index:
            index = section_index[menu['section_name']]
            menu_json = {
                'menu_name': menu['menu_name'],
                'menu_price': menu['menu_price']
            }
            json_list[index]['menus'].append(menu_json)

        else:
            section_menu_json = {
                'section_name': menu['section_name'],
                'menus': [{
                    'menu_name': menu['menu_name'],
                    'menu_price': menu['menu_price']
                }]
            }
            json_list.append(section_menu_json)
            section_index[menu['section_name']] = len(json_list) - 1

    return make_response(json.dumps(json_list, ensure_ascii=False))

#203
@bp.route('/menu/detail')
def delivery_menu_detail():
    if not g.user_id:
        return ('access denied', 500)
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    store_id= request.args['store_id']
    menu_name = request.args['menu_name']

    find={
        '_id': ObjectId(store_id),
    }
    project={
        'menus':{
            '$elemMatch': {'menu_name': menu_name}
        }
    }
    print(db.delivery_store.find_one(find, project))
    menu_detail = db.delivery_store.find_one(find, project)['menus'][0]
    return make_response(json.dumps(menu_detail, ensure_ascii=False))

#포스팅 관련

#204
@bp.route('/post/posting', methods=['POST'])
def delivery_posting():
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
    mongo_db = client['delivery']

    json = request.get_json()
    form = Posting_Form.from_json(json)

    find={'_id': ObjectId(form.store_id.data)}
    projection={'menus': False}
    store = mongo_db.delivery_store.find_one(find,projection)

    today = datetime.now()
    data = {
        'user_id': g.user_id,
        'join_user': [g.user_id],
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
        'orders': []
    }

    print(data)

    _id = mongo_db.delivery_post.insert_one(data)
    post_id = str(_id.inserted_id)

    return jsonify(post_id=post_id)

#206
@bp.route('/post/update', methods=['GET', 'PATCH'])
def delivery_post_update():
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
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
    print(update_data)
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
    db.delivery_post.update_one(find, update)
    return jsonify(post_id=post_id)

#211
@bp.route('/post/join/condition-switch')
def delivery_post_join():
    if not g.user_id:
        return ('access denied', 500)
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    post_id = request.args['post_id']
    find = {
        '_id': ObjectId(post_id)
    }
    post = db.delivery_post.find_one(find)

    if g.user_id == post['user_id']:
        return ('대표자는 그룹을 탈퇴할 수 없습니다', 500)

    if g.user_id in post['join_user']:
        update = {
            '$pull': {
                'join_user': g.user_id
            }
        }
    else:
        update = {
            '$push': {
                'join_user': g.user_id
            }
        }
    db.delivery_post.update_one(find, update)
    return ('', 204)

#213
@bp.route('/post/list')
def delivery_post_list():
    if not g.user_id:
        return ('access denied', 500)
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    projection = {
        'content': False,
        'orders': False
    }
    post_list = list(db.delivery_post.find({}, projection))
    for post in post_list:
        post['_id'] = str(post['_id'])
        post['store']['_id'] = str(post['store']['_id'])
    return make_response(json.dumps(post_list, ensure_ascii=False))

#205
@bp.route('/post/detail/<string:post_id>')
def delivery_post_detail(post_id):
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    find = {
        '_id': ObjectId(post_id)
    }
    update = {
        '$inc': { 'views': 1 }
    }

    post = db.delivery_post.find_one_and_update(find, update, return_document=ReturnDocument.AFTER)

    post['_id'] = str(post['_id'])
    post['store']['_id'] = str(post['store']['_id'])

    return make_response(json.dumps(post, ensure_ascii=False))

#207
@bp.route('/post/condition-switch', methods=['PATCH'])
def delivery_post_condition_switch():
    json = request.get_json()
    post_id = json['post_id']

    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    find = {
        '_id': ObjectId(post_id)
    }
    post = db.delivery_post.find_one(find)

    update = {
        '$set': { 'is_closed' : not post['is_closed'] }
    }
    db.delivery_post.update_one(find, update)

    return jsonify(post_id=post_id)

#주문하기 관련

#209
@bp.route('/ordering', methods=['POST'])
def delivery_ordering():
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    order_json = request.get_json()
    post_id = order_json['post_id']

    orders = pricing(order_json, db)

    user_order = {
        'user_id': g.user_id,
        'orders': orders
    }

    find = {
        '_id': ObjectId(post_id)
    }

    update = {
        '$push': { 'orders': user_order }
    }
    db.delivery_post.update_one(find, update)

    return jsonify(post_id=post_id)

#210
@bp.route('/ordering/update', methods=['GET', 'PATCH'])
def delivery_ordering_update():
    if not g.user_id:
        return ('access denied', 500)

    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    if request.method == 'GET':
        post_id = request.args['post_id']
        find = {
            '_id': ObjectId(post_id)
        }
        projection = {
            'orders': {
                '$elemMatch': {'user_id': g.user_id}
            }
        }
        data = db.delivery_post.find_one(find, projection)
        orders = data['orders'][0]
        return make_response(json.dumps(orders, ensure_ascii=False))

    update_json = request.get_json()
    post_id = update_json['post_id']

    orders = pricing(update_json, db)

    find = {
        '_id': ObjectId(post_id),
        'orders': {
            '$elemMatch': {
                'user_id': g.user_id
            }
        }
    }

    update = {
        '$set': { 'orders.$.orders': orders }
    }

    db.delivery_post.update_one(find, update)

    return ('', 204)
def pricing(order, db):
    store_id = order['store_id']
    orders = order['orders']

    menus = []
    groups = []
    options = []

    for order in orders:
        menus.append(order['menu_name'])
        for group in order['groups']:
            groups.append(group['group_id'])
            options = options + group['options']

    pipe1 = {
        '$match': {
            '_id': ObjectId(store_id)
        }
    }

    pipe2 = {
        '$unwind': '$menus'
    }

    pipe3 = {
        '$unwind': '$menus.groups'
    }

    pipe4 = {
        '$unwind': '$menus.groups.options'
    }

    pipe5 = {
        '$match': {
            'menus.menu_name': {'$in': menus},
            'menus.groups.group_id': {'$in': groups},
            'menus.groups.options.option_id': {'$in': options}
        }
    }
    pipe6 = {
        '$group': {
            '_id': {
                'group_id': '$menus.groups.group_id',
                'menu_name': '$menus.menu_name',
                'menu_price': '$menus.menu_price'
            },
            'group_id': {'$first': '$menus.groups.group_id'},
            "group_name": {'$first': '$menus.groups.group_name'},
            'min_orderable_quantity': {'$first': '$menus.groups.min_orderable_quantity'},
            'max_orderable_quantity': {'$first': '$menus.groups.max_orderable_quantity'},
            'options': {
                '$push': {
                    'option_id': '$menus.groups.options.option_id',
                    'option_name': '$menus.groups.options.option_name',
                    'option_price': '$menus.groups.options.option_price'
                }
            }
        }
    }

    pipe7 = {
        '$group': {
            '_id': '$_id.menu_name',
            'menu_name': {'$first': '$_id.menu_name'},
            'menu_price': {'$first': '$_id.menu_price'},
            'groups': {
                '$push': {
                    "group_id": "$group_id",
                    "group_name": "$group_name",
                    "min_orderable_quantity": "$min_orderable_quantity",
                    "max_orderable_quantity": "$max_orderable_quantity",
                    "options": '$options'
                }
            }
        }
    }

    menu_list = list(db.delivery_store.aggregate([pipe1, pipe2, pipe3, pipe4, pipe5, pipe6, pipe7]))

    def find_option_price(menu_index, group_index, option_id):
        for option in menu_list[menu_index]['groups'][group_index]['options']:
            if option['option_id'] == option_id:
                return option['option_name'], option['option_price']

    def find_group_index(menu_index, group_id):
        for group_index, group in enumerate(menu_list[menu_index]['groups']):
            if group_id == group['group_id']:
                return group_index, group['group_name']

    def find_menu_price(menu_name):
        for menu_index, menu in enumerate(menu_list):
            if menu['menu_name'] == menu_name:
                return menu_index, menu['menu_price']

    for order in orders:
        menu_index, order['menu_price'] = find_menu_price(order['menu_name'])
        for group in order['groups']:
            group_index, group['group_name'] = find_group_index(menu_index, group['group_id'])
            for index, option in enumerate(group['options']):
                option_name, option_price = find_option_price(menu_index, group_index, option)
                option_set = {
                    'option_id': option,
                    'option_name': option_name,
                    'option_price': option_price
                }
                del group['options'][index]
                group['options'].insert(index, option_set)
    return orders