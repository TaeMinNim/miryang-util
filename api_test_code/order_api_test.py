import requests
import json
import pprint
aws_signup = 'http://52.78.106.235:5000/auth/signup'
local_signup = 'http://localhost:5000/auth/signup'


aws_login = 'http://52.78.106.235:5000/auth/login'
local_login = 'http://localhost:5000/auth/login'


aws_posting = 'http://52.78.106.235:5000/order/post/posting'

local_post_detail = 'http://localhost:5000/order/post/detail/633d551c2f1c4e6d47ad3e35'


aws_select = 'http://52.78.106.235:5000/order/'
local_select = 'http://localhost:5000/order/section-menu-select?store_id=2'

local_select_option = 'http://localhost:5000/order/group-option-select?menu_id=1664352908461'

local_post_condition = 'http://localhost:5000/order/post/condition-switch'

loginheader = {
    'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTY2Mzk4OTg4OTgyNiwibmlja19uYW1lIjoiYm9uZyJ9.FULK5UjhV7UnoRa8lUP7MrW0wccROJf9GUp7bac1tvo'
}

logindata = {
    'user_name':'xoals3094',
    'pw' : '~TMwhdkwhdk02'
    
}

signupdata = {
    'user_name':'testID',
    'pw':'testPW',
    'nick_name' : '테스트계정',
    'student_num': '12345'
}

posting = {
    'store_id': '6356cee8b760499670114a7f',
    'title':'이거 조회하세요',
    'content': '같이 시켜요~',
    'order_time': '2022-10-05T10:50',
    'place': '기숙사',
    'min_member' : 3,
    'max_member' : 5
    }

update_posting = {
    'post_id': '6345aa7b911ed10ac4cde368',
    'title':'맘스터치 시키실분자운동',
    'content': '같이 시켜요~',
    'order_time': '2022-10-05T10:50',
    'place': '기숙사',
    'min_member' : 3,
    'max_member' : 5
    }
post_condition = {
    'post_id' : '6345aa7b911ed10ac4cde368'
}

order ={
    'store_id': '6356bba3050d1ddf23347703',
    'post_id': '6356bd1958c02a64dcf06382',
    'orders': [
        {
            #불싸이버거 - 음료변경(제로콜라, 환타, 사이다) - 피클(기본)
            'quantity': 5,
            'menu_name': '싸이버거단품',
            'groups': [
                {
                    'group_id': 1666628558151,
                    'options': [1666628560234]
                }
            ]
        }
    ]
}

update_order ={
    'store_id': '6356bba3050d1ddf23347703',
    'post_id': '6356bd1958c02a64dcf06382',
    'orders': [
        {
            #불싸이버거 - 음료변경(제로콜라, 환타, 사이다) - 피클(기본)
            'quantity': 1,
            'menu_name': '싸이버거단품',
            'groups': [
                {
                    'group_id': 1666628558151,
                    'options': [1666628560234]
                }
            ]
        }
    ]
}
#res = requests.post('http://52.78.106.235:5000/auth/login', json=logindata)

#201
#res = requests.get('http://52.78.106.235:5000/order/store/list', headers=loginheader)

#202
res = requests.get('http://localhost:5000/order/menu/list?store_id=6356cee8b760499670114a7f', headers=loginheader)

#203
#res = requests.get('http://localhost:5000/order/menu/detail?store_id=6356bba3050d1ddf23347703&menu_name=싸이버거단품', headers=loginheader)

#204
#res = requests.post('http://52.78.106.235:5000/order/post/posting', headers=loginheader, json=posting)

#205
#res = requests.get('http://localhost:5000/order/post/detail/6356bd1958c02a64dcf06382', headers=loginheader)

#206
#GET
#res = requests.get('http://localhost:5000/order/post/update?post_id=6345aa7b911ed10ac4cde368', headers=loginheader)
#POST
#res = requests.patch('http://localhost:5000/order/post/update', headers=loginheader, json=update_posting)

#207
#res = requests.patch('http://localhost:5000/order/post/condition-switch', headers=loginheader, json=post_condition)

#209
#res = requests.post('http://localhost:5000/order/ordering', headers=loginheader, json=order)

#210
#GET
#res = requests.get('http://localhost:5000/order/ordering/update?post_id=6356bd1958c02a64dcf06382', headers=loginheader)
#PATCH
#res = requests.patch('http://localhost:5000/order/ordering/update', headers=loginheader, json=update_order)

#res = requests.post(local_signup, json=signupdata)
#res = requests.post(local_login, json=logindata)
#res = requests.post(local_posting, headers=loginheader, json=posting)
#res = requests.get(local_select_option, headers=loginheader)

#res = requests.get('http://localhost:5000/order/post/join/condition-switch?post_id=634e8af7b829facb9e6239e8', headers=loginheader)
#res = requests.get('http://52.78.106.235:5000/order/post/list', headers=loginheader)

#res = requests.get('http://52.78.106.235:5000/order/menu/detail?store_id=6345a45f1c32cd7c4b64d895&menu_name=딥치즈버거', headers=loginheader)



print(res.text)
