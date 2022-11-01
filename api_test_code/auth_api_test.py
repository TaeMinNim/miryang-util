import requests

data = {
    'user_name':'xoals3094',
    'pw': '~TMwhdkwhdk02',
    'nick_name': '찰봉',
    'student_num': 202145807
}

res = requests.post('http://52.78.106.235:5000/auth/signup', json=data)
print(res)
