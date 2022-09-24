from flask_wtf import FlaskForm
from wtforms import Form, StringField, TimeField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email

class Signup_Form(Form):
    user_name = StringField("user_name", [DataRequired()])
    pw = StringField("pw", [DataRequired()])
    nick_name = StringField("nick_name", [DataRequired()])
    student_num = IntegerField("student_num", [DataRequired()])

class Login_Form(FlaskForm):
    user_name = StringField("아이디", [DataRequired()], name="user_name")
    pw = StringField("비밀번호", [DataRequired()], name="pw")
class Create_Group_Form(FlaskForm):
    store = StringField('가게명', [DataRequired()], name="store")
    time = TimeField('시간', [DataRequired()], name="time")
    account_number = StringField('계좌번호', [DataRequired()], name="account-number")
    delivery_cost = IntegerField('배달비', validators=[DataRequired()], name="delivery-cost")

class Order_Form(Form):
    menu = StringField('menu', [DataRequired()])
    quantity = IntegerField('qunatity', [DataRequired()])
    option = StringField('option')
