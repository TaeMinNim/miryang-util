from flask import Blueprint, render_template, g

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html',user_list=User.query.all(), user=g.user)