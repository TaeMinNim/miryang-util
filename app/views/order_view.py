from flask import Blueprint, request, render_template, g, redirect, url_for
from app.forms import Create_Group_Form
from app.models import Order_Group, User
from app import db
from datetime import datetime


import sys

bp = Blueprint('order',__name__, url_prefix='/order')

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

        order_group = Order_Group(
            groupID=groupID,
            store=store,
            time=time,
            delivery_cost=delivery_cost,
            account_number=account_number,
            repUserId=g.user.id)

        db.session.add(order_group)
        db.session.commit()

        g.user.joinGroup=groupID
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('order.order'))
    else:
        return render_template('order/order.html', form=form, group_list=Order_Group.query.all(), user=g.user)

@bp.route('/detail/<int:groupID>')
def detail(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    group = Order_Group.query.get_or_404(groupID)
    repUser = User.query.get(group.repUserId)
    return render_template('order/order_detail.html', user=g.user, group=group, repUser=repUser)

@bp.route('/join/<int:groupID>')
def join(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    group = Order_Group.query.get_or_404(groupID)

    if group:
        g.user.joinGroup = groupID
        db.session.add(g.user)
        db.session.commit()
    return redirect(url_for('order.detail', groupID=groupID))

@bp.route('/quit')
def quit():
    if not g.user:
        return redirect(url_for('main.index'))
    g.user.joinGroup = None
    db.session.commit()
    return redirect(url_for('order.order'))

@bp.route('/delete/<int:groupID>')
def delete(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    group = Order_Group.query.get_or_404(groupID)
    if group.repUserId == g.user.id:
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('order.order'))
    else:
        print("권한이 없습니다", file=sys.stderr)
        return redirect(url_for('order.detail', groupID=groupID))