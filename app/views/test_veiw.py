from flask import Blueprint, request, redirect, url_for, render_template

bp = Blueprint('test', __name__, url_prefix='/test')

API_KEY = 'a3daa2c3fe72cd4cb9b0940afa4451e6'
URL = 'http://13.209.94.41/test/login_kakao'

@bp.route('/login_kakao/', methods=('POST','GET'))
def loginKokao():
    if request.method == 'POST':
        json = request.get_json()
        print(json)
        return redirect(url_for('main.index'))
    else:
        return redirect('https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}'.format(REST_API_KEY=API_KEY, REDIRECT_URI=URL))
