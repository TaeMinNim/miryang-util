import requests

aws_add_store = 'http://52.78.106.235:5000/admin/add-store'
local_add_store = 'http://localhost:5000/admin/add-store'

aws_add_menu = 'http://52.78.106.235:5000/admin/add-menu'
local_add_menu = 'http://localhost:5000/admin/add-menu'


aws_add_group = 'http://52.78.106.235:5000/admin/add-group'
local_add_group = 'http://localhost:5000/admin/add-group'

aws_add_option = 'http://52.78.106.235:5000/admin/add-option'
local_add_option = 'http://localhost:5000/admin/add-option'


store={
    'store_name': '맘스터치',
    'fee': 3000,
    'min_order': 12000
}

menu={
    'store_id': '6356cee8b760499670114a7f',
    'section_name': '단품메뉴',
    'menu_name': '싸이버거단품',
    'menu_price': 50000
}

group={
    'store_id': '6356cee8b760499670114a7f',
    'section_name': '단품메뉴',
    'menu_name': '싸이버거단품',
    'group_name': '피클',
    'min_orderable_quantity': 1,
    'max_orderable_quantity': 1
}

option={
    'store_id': '6356cee8b760499670114a7f',
    'section_name': '단품메뉴',
    'menu_name': '싸이버거단품',
    'group_name': '피클',
    'option_name': '빼기',
    'option_price': 50000000   
}


#requests.post(aws_add_store, json=store)
#requests.post(aws_add_menu,json=menu)
#requests.post(aws_add_group,json=group)
requests.post(aws_add_option,json=option)

