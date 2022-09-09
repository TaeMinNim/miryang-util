from app import db

class User(db.Model):
    __tablename__="USER"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    joinGroup = db.Column(db.Integer, db.ForeignKey('GROUP.id', ondelete='SET NULL'))

class Group(db.Model):
    __tablename__ = "GROUP"
    id = db.Column(db.Integer, primary_key=True)
    repUserId = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='CASCADE'))
    repUser = db.relationship('User', foreign_keys=[repUserId], backref=db.backref('repGroup', cascade='all, delete'), passive_deletes=True)

    joinuser = db.Column(db.Integer)
    store = db.Column(db.String(50))
    time = db.Column(db.DateTime())
    delivery_cost = db.Column(db.Integer)
    account_number = db.Column(db.String(50))

class Order(db.Model):
    __tablename__="ORDER"
    id = db.Column(db.Integer, primary_key=True)
    groupID = db.Column(db.Integer, db.ForeignKey('GROUP.id', ondelete='CASCADE'))
    userID = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='CASCADE'))

    menu = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    option = db.Column(db.String(50), nullable=True)

    user = db.relationship('User', foreign_keys=[userID], backref=db.backref('order', cascade='all, delete'), passive_deletes=True)
    group = db.relationship('Group', foreign_keys=[groupID], backref=db.backref('order', cascade='all, delete'), passive_deletes=True)
'''
class D_Store(db.Model):
    __tablename__ = "D_STORE"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    fee = db.Column(db.Integer, nullable=False)

class D_Menu(db.Model):
    __tablename__ = "D_MENU"
    id = db.Column(db.Integer, primary_key=True)
    storeID = db.Column(db.Integer, db.ForeignKey('D_STORE.id'))
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class D_Option(db.Model):
    __talbename__ = "D_OPTION"
    id = db.Column(db.Integer, primary_kye=True)
    optionID = db.Column(db.Integer, db.ForeignKey('D_MENU.id'))
class D_Group(db.Model):
    __tablename__ = "D_GROUP"
    id = db.Column(db.Integer, primary_key=True)
    repID = db.Column(db.Integer, db.ForeignKey('USER.id'))
    storeID = db.Column(db.Integer, db.ForeignKey('D_STORE.id'))

    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text(), nullable=True)
    order_time = db.Column(db.DateTime(), nullable=False)
    min_member = db.Column(db.Integer, nullable=True)
    cur_member = db.Column(db.Integer, nullable=False)
    max_member = db.Column(db.Integer, nullable=True)
    is_closed = db.Column(db.Boolean, nullable=False)

class Order_Menu(db.Model):
    __tablename__ = "ORDER_MENU"
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('USER.id'))
    groupID = db.Column(db.Integer, db.ForeignKey('D_GROUP.id'))
    menuID = db.Column(db.Integer, db.ForeignKey('D_MENU.id'))

class Order_Option(db.Model):
    __tablename__ = "ORDER_OPTION"
    id = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('ORDER_MENU.id'))
    optionID = db.Column(db.Integer, db.ForeignKey('D_OPTION.id'))
    quantity = db.Column(db.Integer, nullable=False)
'''

'''class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('USER.id'))
    groupID = db.Column(db.Integer, db.ForeignKey('D_GROUP.id'))
    menuID = db.Column(db.Integer, db.ForeignKey('D_MENU.id'))'''




