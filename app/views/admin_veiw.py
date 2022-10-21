from flask import Blueprint, request
from app.forms import Add_Store_Form, Add_Menu_Form,Add_Group_Form,Add_Option_Form
from app import db_connection
import wtforms_json
from datetime import datetime


from bson.objectid import  ObjectId
from pymongo import MongoClient

bp = Blueprint('admin',__name__, url_prefix='/admin')
wtforms_json.init()

@bp.route('/add-store', methods=['POST'])
def add_store():
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    json = request.get_json()
    print(json)
    form = Add_Store_Form.from_json(json)

    data = {
        'store_name' : form.store_name.data,
        'fee' : form.fee.data,
        'min_order' : form.min_order.data,
        'menus' : []
    }

    _id = db.delivery_store.insert_one(data)
    return (str(_id.inserted_id), 200)

@bp.route('/add-menu', methods=['POST'])
def add_menu():
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    json = request.get_json()
    print(json)
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
    return ('', 204)

@bp.route('/add-group', methods=['POST'])
def add_group():
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']

    json = request.get_json()
    print(json)
    form = Add_Group_Form.from_json(json)
    store_id = form.store_id.data
    id = int(round(datetime.today().timestamp() * 1000))
    data = {
        'group_id': id,
        'group_name': form.group_name.data,
        'min_orderable_quantity': form.min_orderable_quantity.data,
        'max_orderable_quantity': form.max_orderable_quantity.data,
        'options': []
    }
    find = {'_id': ObjectId(store_id)}

    update={
        '$push': {'menus.$[m].groups': data}
    }

    identifier=[
        {'m.menu_name': form.menu_name.data}
    ]
    db.delivery_store.update_many(filter=find, update=update, array_filters=identifier)

    return ('', 204)

@bp.route('/add-option', methods=['POST'])
def add_option():
    client = MongoClient(host='localhost', port=27017)
    db = client['delivery']
    json = request.get_json()
    print(json)
    form = Add_Option_Form.from_json(json)

    store_id = form.store_id.data
    id = int(round(datetime.today().timestamp() * 1000))
    data = {
        'option_id': id,
        'option_name': form.option_name.data,
        'option_price': form.option_price.data
    }

    find={'_id': ObjectId(store_id)}

    update={
        '$push': {'menus.$[m].groups.$[g].options': data}
    }

    identifier=[
            {'m.menu_name': form.menu_name.data},
            {'g.group_name': form.group_name.data}
    ]

    db.delivery_store.update_many(filter=find, update=update, array_filters=identifier)
    return ('', 204)