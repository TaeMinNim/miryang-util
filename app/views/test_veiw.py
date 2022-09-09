from flask import Blueprint, request


bp = Blueprint('test', __name__, url_prefix='/test/')

@bp.route('/')
def order_test():
