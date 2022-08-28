from app import db

class User(db.Model):
    __tablename__="USER"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    joinGroup = db.Column(db.Integer, db.ForeignKey('ORDER_GROUP.groupID', ondelete="CASCADE"))
    group = db.relationship('Order_Group', foreign_keys=[joinGroup],backref=db.backref('joined_user'))

class Order_Group(db.Model):
    __tablename__ = "ORDER_GROUP"
    groupID = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(50))
    time = db.Column(db.DateTime())
    delivery_cost = db.Column(db.Integer)
    account_number = db.Column(db.String(50))
    repUserId = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete="CASCADE"))