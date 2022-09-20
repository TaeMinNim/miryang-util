from flask_wtf import FlaskForm
from wtforms import Form, StringField, TimeField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email

class Signup_Form(FlaskForm):
    username = StringField("아이디", [DataRequired()], name="username")
    pw = StringField("비밀번호", [DataRequired()], name="pw")
    nickname = StringField("닉네임", [DataRequired()], name="nickname")
    email = EmailField("이메일", [DataRequired()], name="email")

class Create_Group_Form(FlaskForm):
    store = StringField('가게명', [DataRequired()], name="store")
    time = TimeField('시간', [DataRequired()], name="time")
    account_number = StringField('계좌번호', [DataRequired()], name="account-number")
    delivery_cost = IntegerField('배달비', validators=[DataRequired()], name="delivery-cost")

class Order_Form(Form):
    menu = StringField('menu', [DataRequired()])
    quantity = IntegerField('qunatity', [DataRequired()])
    option = StringField('option')

class SignUP_Form(Form):
    userID = StringField('userID', [DataRequired()])
    email = EmailField('email', [DataRequired(), Email()])
