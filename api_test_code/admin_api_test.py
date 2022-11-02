import requests

aws_add_store = 'http://52.78.106.235:5000/admin/delivery/add/store'
local_add_store = 'http://localhost:5000/admin/delivery/add/store'

aws_add_menu = 'http://52.78.106.235:5000/admin/delivery/add/menu'
local_add_menu = 'http://localhost:5000/admin/delivery/add/menu'


aws_add_group = 'http://52.78.106.235:5000/admin/delivery/add/group'
local_add_group = 'http://localhost:5000/admin/delivery/add/group'

aws_add_option = 'http://52.78.106.235:5000/admin/delivery/add/option'
local_add_option = 'http://localhost:5000/admin/delivery/add/option'


store={
    'store_name': '맘스터치',
    'fee': 3000,
    'min_order': 12000
}

menu={
    'store_id': '63629389fe982026b114a2eb',
    'section_name': '단품메뉴',
    'menu_name': '싸이버거단품',
    'menu_price': 50000
}

menu={
    'store_id': '63629389fe982026b114a2eb',
    'section_name': '세트메뉴',
    'menu_name': '싸이버거세트',
    'menu_price': 4000
}

group={
    'store_id': '63629389fe982026b114a2eb',
    'section_name': '세트메뉴',
    'menu_name': '불싸이버거세트',
    'groups': [
        {
            'group_name': '피클',
            'min_orderable_quantity': 1,
            'max_orderable_quantity': 1
        },
        {
            'group_name': '음료변경',
            'min_orderable_quantity': 1,
            'max_orderable_quantity': 1
        }
    ]
}

option={
    'store_id': '63629389fe982026b114a2eb',
    'section_name': '세트메뉴',
    'menu_name': '싸이버거세트',
    'group_id': '6465410e-cfd2-4ed0-940f-09b69a1f9f7c',
    'options':[
        {
            'option_name': '빼기',
            'option_price': 50000000
        },
        {
            'option_name': '기본',
            'option_price': 0
        }
     ]       
}
'''
option={
    'store_id': '63629389fe982026b114a2eb',
    'section_name': '세트메뉴',
    'menu_name': '불싸이버거세트',
    'group_id': 'e156ecf1-289f-426f-a072-b4eea130cd9c',
    'options':[
        {
            'option_name': '제로콜라',
            'option_price': 50000000
        },
        {
            'option_name': '펩시콜라',
            'option_price': 0
        },
        {
            'option_name': '코카콜라',
            'option_price': 50000
        },
        {
            'option_name': '사이다',
            'option_price': 1000
        }
        
     ]       
}'''

platform = { 'platform_name' : '기숙사' }


#res = requests.post(aws_add_store, json=store)
#res = requests.post(aws_add_menu,json=menu)
#res = requests.post(aws_add_group,json=group)
res = requests.post(aws_add_option,json=option)

#requests.post('http://localhost:5000/admin/taxi/platform',json=platform)
print(res.text)
