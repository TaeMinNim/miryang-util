from flask import Blueprint, redirect, request, url_for
import requests
from werkzeug.wrappers import response

bp = Blueprint('test', __name__, url_prefix='/test')

API_KEY = 'a3daa2c3fe72cd4cb9b0940afa4451e6'
URL = 'http://localhost:5000/test/kakao/code'
#URL = 'http://13.209.94.41/test/login_kakao'



@bp.route('/login_kakao/')
def loginKokao():
    return redirect('https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}'.format(REST_API_KEY=API_KEY, REDIRECT_URI=URL))

@bp.route('/kakao/code')
def test():
    return redirect(url_for('test.token', code=request.args['code']))

@bp.route('/token_kakao/<code>')
def token(code):
    header = { 'Content-Type': 'application/x-www-form-urlencoded' }
    data = {
        'grant_type' : 'authorization_code',
        'client_id' : API_KEY,
        'redirect_uri' : URL,
        'code' : code,
        'client_secret' : 'l5gasv3tCZu8itjxHMhn6TwqgUubmgGe'
    }
    res = requests.post('https://kauth.kakao.com/oauth/token', headers=header, data=data)
    return redirect(url_for('test.getuser', token=res.json()['access_token']))

@bp.route('/getuser/<token>')
def getuser(token):
    header = {
        'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization' : 'Bearer {token}'.format(token=token) }
    res = requests.get(url='https://kapi.kakao.com/v2/user/me', headers=header)
    return '너의 이메일은 ' + res.json()['kakao_account']['email'] + ' 넌 이제 해킹당했다 우하하하'
