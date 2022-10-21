from flask_wtf import FlaskForm
from wtforms import Form, StringField, TimeField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email

class Signup_Form(Form):
    user_name = StringField("user_name", [DataRequired()])
    pw = StringField("pw", [DataRequired()])
    nick_name = StringField("nick_name", [DataRequired()])
    student_num = IntegerField("student_num", [DataRequired()])

class Login_Form(Form):
    user_name = StringField("user_name", [DataRequired()])
    pw = StringField("pw", [DataRequired()])

class Posting_Form(Form):
    store_id = StringField('store_id', [DataRequired()])
    title = StringField('title', [DataRequired()])
    content = TextAreaField('content')
    place = StringField('place', [DataRequired()])
    order_time = StringField('order_time', [DataRequired()])
    min_member = IntegerField('min_member', [DataRequired()])
    max_member = IntegerField('max_member', [DataRequired()])

class Order_Form(Form):
    count = IntegerField('count', [DataRequired()])
    menu_id = IntegerField('menu_id', [DataRequired()])


class Add_Store_Form(Form):
    store_name = StringField('store_name', [DataRequired()])
    fee = IntegerField('fee', [DataRequired()])
    min_order = IntegerField('min_order', [DataRequired()])


class Add_Menu_Form(Form):
    store_id = StringField('store_id', [DataRequired()])
    section_name = StringField('section_name', [DataRequired()])
    menu_name = StringField('menu_name', [DataRequired()])
    menu_price = IntegerField('menu_price', [DataRequired()])

class Add_Group_Form(Form):
    store_id = StringField('store_id', [DataRequired()])
    section_name = StringField('section_name', [DataRequired()])
    menu_name = StringField('menu_name', [DataRequired()])
    group_name = StringField('group_name', [DataRequired()])
    min_orderable_quantity = IntegerField('min_orderable_quantity', [DataRequired()])
    max_orderable_quantity = IntegerField('max_orderable_quantity', [DataRequired()])
class Add_Option_Form(Form):
    store_id = StringField('store_id', [DataRequired()])
    section_name = StringField('section_name', [DataRequired()])
    menu_name = StringField('menu_name', [DataRequired()])
    group_name = StringField('group_name', [DataRequired()])
    option_name = StringField('option_name', [DataRequired()])
    option_price = IntegerField('option_price', [DataRequired()])
