from flask import Blueprint, request, g, redirect, url_for, make_response
from app.forms import Posting_Form
from datetime import datetime
import wtforms_json
from app import db_connection
import json

bp = Blueprint('order',__name__, url_prefix='/order')
wtforms_json.init()

@bp.route('/posting', methods=['POST'])
def delivery_posting():
    if not g.user_id:
        return ('access denied', 500)
    db = db_connection()
    cursor = db.cursor()

    json = request.get_json()
    print(json)
    form = Posting_Form.from_json(json)

    today = datetime.today()
    print(datetime.now())
    id = int(round(today.timestamp() * 1000))
    sql = """
    INSERT INTO DELIVERY_POST (id, user_id, store_id, title, content, order_time, current_member, min_member, max_member, is_closed)
    VALUE({id}, {user_id}, {store_id}, '{title}', '{content}', '{order_time}', {current_member}, {min_member}, {max_member}, {is_closed})""".format(
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
    print(sql)
    cursor.execute(sql)
    db.commit()
    db.close()
    return ('',204)

@bp.route('/store-list')
def delivery_select():
    if not g.user_id:
        return ('access denied', 500)
    db = db_connection()
    cursor = db.cursor()
    sql = '''SELECT id, store_name, fee FROM DELIVERY_STORE'''

    cursor.execute(sql)
    list = cursor.fetchall()
    db.close()
    response_json = []
    for data in list:
        response_json.append({'store_id' : data[0],
                              'store_name' : data[1],
                              'fee' : data[2]})
        response = make_response(json.dumps(response_json))
    return response

@bp.route('/section-menu-select')
def delivery_section_menu_select():
    if not g.user_id:
        return ('access denied', 500)
    db = db_connection()
    cursor = db.cursor()
    store_id = request.args['store_id']

    menu_list_sql = '''
    WITH 
    section_selected AS (
        SELECT * 
        FROM delivery_section 
            WHERE store_id = {store_id}
        )
    SELECT 
        S.id as section_id, 
        S.section_name, M.id as menu_id, 
        M.menu_name,
        M.price  
    FROM section_selected S JOIN  delivery_menu M ON (S.id = M.section_id)
    '''.format(store_id=store_id)

    cursor.execute(menu_list_sql)
    menu_list = cursor.fetchall()
    section_menu_list = []
    section_index = {}
    def create_menu(menu_id, menu_name, menu_price):
        menu = {
            'menu_id': menu_id,
            'menu_name': menu_name,
            'menu_price': menu_price
        }
        return menu
    def create_section(section_id, section_name, menu):
        section_menu = {
            'section_id': section_id,
            'section_name': section_name,
            'menu_list': [menu]
        }
        return section_menu

    for menu in menu_list:
        section_id = menu[0]
        section_name = menu[1]
        menu_id = menu[2]
        menu_name = menu[3]
        menu_price = menu[4]
        if section_id in section_index:
            menu = create_menu(menu_id, menu_name, menu_price)
            index = section_index[section_id]
            section_menu_list[index]['menu_list'].append(menu)
        else:
            section = create_section(section_id, section_name, create_menu(menu_id, menu_name, menu_price))
            section_menu_list.append(section)
            section_index[section_id] = len(section_menu_list) - 1

    return make_response(json.dumps(section_menu_list))

@bp.route('/group-option-select')
def delivery_group_option_select():
    if not g.user_id:
        return ('access denied', 500)
    db = db_connection()
    cursor = db.cursor()
    menu_id = request.args['menu_id']

    menu_list_sql = '''
    WITH 
    group_selected AS (
        SELECT 
            id,
            group_name,
            min_orderable_quantity,
            max_orderable_quantity
        FROM delivery_group
            WHERE menu_id = {menu_id}
        ),
    group_option_mapping AS (
        SELECT 
            G.id AS group_id, 
            G.group_name,
            G.min_orderable_quantity,
            G.max_orderable_quantity,
            MAP.option_id 
        FROM group_selected G JOIN delivery_option_group_mapping MAP 
            ON (G.id = MAP.group_id)
        )
    SELECT 
        MAP.group_id, 
        MAP.group_name, 
        MAP.min_orderable_quantity,
        MAP.max_orderable_quantity,
        O.id AS option_id,
        O.option_name,
        O.price
    FROM group_option_mapping MAP JOIN delivery_option O
        ON (MAP.option_id = O.id)
    '''.format(menu_id=menu_id)

    cursor.execute(menu_list_sql)
    option_list = cursor.fetchall()


    def create_option(option_id, option_name, option_price):
        option = {
            'option_id': option_id,
            'option_name': option_name,
            'option_price': option_price
        }
        return option
    def create_group(group_id, group_name, min_orderable_quantity, max_orderable_quantity, option):
        group_option = {
            'group_id': group_id,
            'group_name': group_name,
            'min_orderable_quantity' : min_orderable_quantity,
            'max_orderable_quantity' : max_orderable_quantity,
            'option_list': [option]
        }
        return group_option

    group_option_list = []
    group_index = {}
    for option in option_list:
        group_id = option[0]
        group_name = option[1]
        min_orderable_quantity = option[2]
        max_orderable_quantity = option[3]
        option_id = option[4]
        option_name = option[5]
        option_price = option[6]
        if group_id in group_index:
            option = create_option(option_id, option_name, option_price)
            index = group_index[group_id]
            group_option_list[index]['option_list'].append(option)
        else:
            group = create_group(group_id, group_name, min_orderable_quantity, max_orderable_quantity,
                                   create_option(option_id, option_name, option_price))
            group_option_list.append(group)
            group_index[group_id] = len(group_option_list) - 1

    return make_response(json.dumps(group_option_list))

