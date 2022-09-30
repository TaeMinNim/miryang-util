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
    store_id = IntegerField('store_id', [DataRequired()])
    title = StringField('title', [DataRequired()])
    content = TextAreaField('content')
    min_member = IntegerField('min_member', [DataRequired()])
    max_member = IntegerField('max_member', [DataRequired()])


class Add_Store_Form(Form):
    store_name = StringField('store_name', [DataRequired()])
    fee = IntegerField('fee', [DataRequired()])
    min_order = IntegerField('min_order', [DataRequired()])

class Add_Section_Form(Form):
    store_id = IntegerField('store_id', [DataRequired()])
    section_name = StringField('section_name', [DataRequired()])

class Add_Menu_Form(Form):
    store_id = IntegerField('store_id', [DataRequired()])
    section_id = IntegerField('section_id', [DataRequired()])
    menu_name = StringField('menu_name', [DataRequired()])
    price = IntegerField('price', [DataRequired()])

class Add_Group_Form(Form):
    menu_id = IntegerField('menu_id', [DataRequired()])
    group_name = StringField('area_name', [DataRequired()])
    min_orderable_quantity = IntegerField('min_orderable_quantity', [DataRequired()])
    max_orderable_quantity = IntegerField('max_orderable_quantity', [DataRequired()])
class Add_Option_Form(Form):
    store_id = IntegerField('store_id', [DataRequired()])
    area_id = IntegerField('area_id', [DataRequired()])
    option_name = StringField('option_name', [DataRequired()])
    price = IntegerField('price', [DataRequired()])

class Add_Option_Group_Mapping_Form(Form):
    group_id = IntegerField('group_id', [DataRequired()])
    option_id = IntegerField('option_id', [DataRequired()])