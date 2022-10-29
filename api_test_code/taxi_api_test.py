import requests
loginheader = {
    'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTY2Mzk4OTg4OTgyNiwibmlja19uYW1lIjoiYm9uZyJ9.FULK5UjhV7UnoRa8lUP7MrW0wccROJf9GUp7bac1tvo'
}
posting = {
    'title':'이거 조회하세요',
    'content': '같이 타요~',
    'depart_time': '2022-10-05T10:50',
    'depart_name': '기숙사',
    'dest_name': '밀양역',
    'min_member' : 3,
    'max_member' : 5
    }


#res = requests.get('http://localhost:5000/taxi/platform/list')
res = requests.post('http://localhost:5000/taxi/post/posting',json=posting, headers=loginheader)
print(res.text)
