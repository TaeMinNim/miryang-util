from flask import Blueprint, request, jsonify
from app.forms import Add_Store_Form, Add_Menu_Form
from app import mongodb_connection
import wtforms_json
from datetime import datetime

from bson.objectid import ObjectId
from pymongo import MongoClient

bp = Blueprint('admin',__name__, url_prefix='/admin')
wtforms_json.init()

@bp.route('/delivery/add/store', methods=['POST'])
def add_delivery_store():
    client = mongodb_connection()
    db = client['delivery']

    json = request.get_json()
    form = Add_Store_Form.from_json(json)

    data = {
        'store_name': form.store_name.data,
        'fee': form.fee.data,
        'min_order': form.min_order.data,
        'menus': []
    }

    _id = db.delivery_store.insert_one(data)
    return jsonify(store_id=str(_id.inserted_id))

@bp.route('/delivery/add/menu', methods=['POST'])
def add_delivery_menu():
    client = mongodb_connection()
    db = client['delivery']

    json = request.get_json()
    form = Add_Menu_Form.from_json(json)

    store_id = form.store_id.data

    find = {
        '_id': ObjectId(store_id),
    }

    data = {
        'section_name': form.section_name.data,
        'menu_name': form.menu_name.data,
        'menu_price': form.menu_price.data,
        'groups': []
    }
    db.delivery_store.update_one(find, {'$push': {'menus': data}})
    return jsonify(menu_name=form.menu_name.data)

@bp.route('/delivery/add/group', methods=['POST'])
def add_delivery_group():
    client = mongodb_connection()
    db = client['delivery']

    insert_json_data = request.get_json()
    store_id = insert_json_data['store_id']

    group_list = []
    group_ids = []
    for group in insert_json_data['groups']:
        id = int(round(datetime.today().timestamp() * 1000))
        group_ids.append(id)

        group['group_id'] = id
        group_list.append(group)

    find = {'_id': ObjectId(store_id)}

    update={
        '$push': {'menus.$[m].groups': {'$each': group_list}}
    }

    identifier=[
        {'m.menu_name': insert_json_data['menu_name']}
    ]
    db.delivery_store.update_many(filter=find, update=update, array_filters=identifier)

    return jsonify(group_ids=group_ids, menu_name=insert_json_data['menu_name'])

@bp.route('/delivery/add/option', methods=['POST'])
def add_delivery_option():
    client = mongodb_connection()
    db = client['delivery']
    insert_json_data = request.get_json()

    store_id = insert_json_data['store_id']

    option_list = []
    option_ids = []
    for option in insert_json_data['options']:
        id = int(round(datetime.today().timestamp() * 1000))
        option_ids.append(id)

        option['option_id'] = id
        option_list.append(option)

    find = {'_id': ObjectId(store_id)}

    update={
        '$push': {'menus.$[m].groups.$[g].options': {'$each': option_list}}
    }

    identifier=[
        {'m.menu_name': insert_json_data['menu_name']},
        {'g.group_id': insert_json_data['group_id']}
    ]

    db.delivery_store.update_many(filter=find, update=update, array_filters=identifier)
    return jsonify(option_ids=option_ids)

@bp.route('/taxi/platform', methods=['POST'])
def taxi_platform():
    client = mongodb_connection()
    db = client['taxi']

    json = request.get_json()

    data = {
        'platform_name': json['platform_name']
    }

    _id = db.taxi_platform.insert_one(data)
    return (str(_id.inserted_id), 200)