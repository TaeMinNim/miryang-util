from flask import Blueprint, request, render_template, g, redirect, url_for
from app.forms import Create_Group_Form, Order_Form
from app.models import Group, User, Order
from app import db
from datetime import datetime
import wtforms_json

import sys

bp = Blueprint('order',__name__, url_prefix='/order')
wtforms_json.init()
@bp.route('/', methods=('GET', 'POST'))
def order():
    if not g.user:
        return redirect(url_for('main.index'))
    form = Create_Group_Form()
    if request.method == 'POST' and form.validate_on_submit():
        today = datetime.today()
        groupID = int(round(today.timestamp() * 1000))
        store = form.store.data
        time = form.time.data
        delivery_cost = form.delivery_cost.data
        account_number = form.account_number.data

        time = datetime(today.year, today.month, today.day, time.hour, time.minute)

        group = Group(
            id=groupID,
            joinuser=1,
            store=store,
            time=time,
            delivery_cost=delivery_cost,
            account_number=account_number,
            repUserId=g.user.id)

        db.session.add(group)
        db.session.commit()

        g.user.joinGroup=groupID
        db.session.add(g.user)
        db.session.commit()

        return redirect(url_for('order.order'))
    else:
        return render_template('order/order.html', form=form, group_list=Group.query.all(), user=g.user)

@bp.route('/detail/<int:groupID>', methods=('GET', 'POST'))
def detail(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        json = request.get_json()
        print(json)
        count = 0
        for order in json:
            count += 1
            print(order['formdata'])
            form = Order_Form.from_json(order['formdata'])
            today = datetime.today()
            id = int(round(today.timestamp() * 1000))
            order = Order(
                id = id + count,
                groupID = groupID,
                userID = g.user.id,
                menu = form.menu.data,
                quantity = form.quantity.data,
                option = form.option.data)
            db.session.add(order)
        db.session.commit()
        return ('', 204)
    else:
        group = Group.query.get_or_404(groupID)
        repUser = User.query.get(group.repUserId)
        join_user = User.query.filter_by(joinGroup=group.id).all()
        return render_template('order/order_detail.html', user=g.user, group=group, repUser=repUser, join_user=join_user)

@bp.route('/join/<int:groupID>')
def join(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    group = Group.query.get_or_404(groupID)

    if group:
        group.joinuser += 1
        g.user.joinGroup = groupID
        db.session.commit()
    return redirect(url_for('order.detail', groupID=groupID))

@bp.route('/quit')
def quit():
    if not g.user:
        return redirect(url_for('main.index'))
    g.user.order
    g.user.joinGroup = None
    Order.query.filter_by(userID=g.user.id).delete()
    db.session.commit()
    return redirect(url_for('order.order'))

@bp.route('/delete/<int:groupID>')
def delete(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    group = Group.query.get_or_404(groupID)
    if group.repUserId == g.user.id:
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('order.order'))
    else:
        print("권한이 없습니다", file=sys.stderr)
        return redirect(url_for('o  rder.detail', groupID=groupID))