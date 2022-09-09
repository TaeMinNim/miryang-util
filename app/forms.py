from flask_wtf import FlaskForm
from wtforms import Form, StringField, TimeField, IntegerField
from wtforms.validators import DataRequired

class Login_Form(FlaskForm):
    username = StringField("이름", [DataRequired()], name="username")
    nickname = StringField("닉네임", [DataRequired()], name="nickname")

class Create_Group_Form(FlaskForm):
    store = StringField('가게명', [DataRequired()], name="store")
    time = TimeField('시간', [DataRequired()], name="time")
    account_number = StringField('계좌번호', [DataRequired()], name="account-number")
    delivery_cost = IntegerField('배달비', validators=[DataRequired()], name="delivery-cost")

class Order_Form(Form):
    menu = StringField('menu', [DataRequired()])
    quantity = IntegerField('qunatity', [DataRequired()])
    option = StringField('option')

