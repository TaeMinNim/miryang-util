from flask import Blueprint, request, render_template


bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/signup/', methods=('POST','GET'))
def signup():
    if request.method == 'POST':
        json = request.get_json()
        print(json)
        return ('', 204)
    else:
        return render_template('auth/test_signup_form.html')
