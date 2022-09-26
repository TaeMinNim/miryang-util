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
class Create_Group_Form(FlaskForm):
    store = StringField('가게명', [DataRequired()], name="store")
    time = TimeField('시간', [DataRequired()], name="time")
    account_number = StringField('계좌번호', [DataRequired()], name="account-number")
    delivery_cost = IntegerField('배달비', validators=[DataRequired()], name="delivery-cost")

class Posting_Form(Form):
    store_id = IntegerField('store_id', [DataRequired()])
    title = StringField('title', [DataRequired()])
    content = TextAreaField('content')
    min_member = IntegerField('min_member', [DataRequired()])
    max_member = IntegerField('max_member', [DataRequired()])


class Order_Form(Form):
    menu = StringField('menu', [DataRequired()])
    quantity = IntegerField('qunatity', [DataRequired()])
    option = StringField('option')
