from flask import Blueprint, request
from app.forms import Add_Store_Form, Add_Section_Form, Add_Menu_Form,Add_Group_Form,Add_Option_Form, Add_Option_Group_Mapping_Form
from app import db_connection
import wtforms_json
from datetime import datetime
bp = Blueprint('admin',__name__, url_prefix='/admin')
wtforms_json.init()


@bp.route('/add-store', methods=['POST'])
def add_store():
    json = request.get_json()
    print(json)
    form = Add_Store_Form.from_json(json)
    id = int(round(datetime.today().timestamp() * 1000))
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO delivery_store (id, store_name, fee, min_order) 
    VALUE({id}, '{store_name}', {fee}, {min_order})
    """.format(id=id, store_name=form.store_name.data, fee=form.fee.data, min_order=form.min_order.data)

    cursor.execute(sql)

    db.commit()
    db.close()
    return ('', 204)

@bp.route('/add-section', methods=['POST'])
def add_section():
    json = request.get_json()
    print(json)
    form = Add_Section_Form.from_json(json)
    id = int(round(datetime.today().timestamp() * 1000))
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO delivery_menu_section (id, store_id, section_name) 
    VALUE({id}, {store_id}, '{section_name}')
    """.format(id=id, store_id=form.store_id.data, section_name=form.section_name.data)

    cursor.execute(sql)

    db.commit()
    db.close()
    return ('', 204)

@bp.route('/add-menu', methods=['POST'])
def add_menu():
    json = request.get_json()
    print(json)
    form = Add_Menu_Form.from_json(json)
    id = int(round(datetime.today().timestamp() * 1000))
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO delivery_menu (id, store_id, section_id, menu_name, price) 
    VALUE({id}, {store_id}, {section_id}, '{menu_name}', {price})
    """.format(id=id, store_id=form.store_id.data, section_id=form.section_id.data, menu_name=form.menu_name.data, price=form.price.data)

    cursor.execute(sql)

    db.commit()
    db.close()
    return ('', 204)

@bp.route('/add-group', methods=['POST'])
def add_area():
    json = request.get_json()
    print(json)
    form = Add_Group_Form.from_json(json)
    id = int(round(datetime.today().timestamp() * 1000))
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO delivery_group (id, menu_id, group_name, min_orderable_quantity, max_orderable_quantity) 
    VALUE({id}, {menu_id}, '{group_name}', {min_orderable_quantity}, {max_orderable_quantity})
    """.format(id=id, menu_id=form.menu_id.data, group_name=form.group_name.data,
               min_orderable_quantity=form.min_orderable_quantity.data, max_orderable_quantity=form.max_orderable_quantity.data)
    cursor.execute(sql)

    db.commit()
    db.close()
    return ('', 204)

@bp.route('/add-option-group-mapping', methods=['POST'])
def add_area_to_menu():
    json = request.get_json()
    print(json)
    form = Add_Option_Group_Mapping_Form.from_json(json)
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO delivery_option_group_mapping (group_id, option_id) 
    VALUE({group_id}, '{option_id}')
    """.format(group_id=form.group_id.data, option_id=form.option_id.data)
    cursor.execute(sql)

    db.commit()
    db.close()
    return ('', 204)

@bp.route('/add-option', methods=['POST'])
def add_option():
    json = request.get_json()
    print(json)
    form = Add_Option_Form.from_json(json)
    id = int(round(datetime.today().timestamp() * 1000))
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO delivery_option (id, option_name, price) 
    VALUE({id}, '{option_name}', {price})
    """.format(id=id, option_name=form.option_name.data, price=form.price.data)
    cursor.execute(sql)

    db.commit()
    db.close()
    return ('', 204)