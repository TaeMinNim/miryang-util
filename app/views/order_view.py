from flask import Blueprint, request, render_template, g, redirect, url_for
from app.forms import Create_Group_Form, Order_Form
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

        return redirect(url_for('order.order'))

@bp.route('/detail/<int:groupID>', methods=('GET', 'POST'))
def detail(groupID):
    if not g.user:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        json = request.get_json()
        for order in json:
            form = Order_Form.from_json(order['formdata'])
            today = datetime.today()
            id = int(round(today.timestamp() * 1000))
        return ('', 204)
