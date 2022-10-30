import requests
loginheader = {
    'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTY2Mzk4OTg4OTgyNiwibmlja19uYW1lIjoiYm9uZyJ9.FULK5UjhV7UnoRa8lUP7MrW0wccROJf9GUp7bac1tvo'
}
posting = {
    'title':'이거 조회하세요 초 있는 버전',
    'content': '같이 타요~',
    'depart_time': '2022-10-05T10:50:20',
    'depart_name': '기숙사',
    'dest_name': '밀양역',
    'min_member' : 3,
    'max_member' : 5
    }

condition = {
    'post_id':'635cbd183753f9469ac717ee'
    }

#res = requests.get('http://localhost:5000/taxi/platform/list')
res = requests.post('http://52.78.106.235:5000/taxi/post/posting',json=posting, headers=loginheader)
#res = requests.get('http://localhost:5000/taxi/post/detail/635cbd183753f9469ac717ee',headers=loginheader)
#res = requests.patch('http://localhost:5000/taxi/post/condition-switch',headers=loginheader, json=condition)
#res = requests.patch('http://localhost:5000/taxi/post/join/condition-switch',headers=loginheader, json=condition)
#res = requests.get('http://52.78.106.235:5000/taxi/post/list',headers=loginheader)
print(res.text)
