from flask import Blueprint, make_response,g ,request
from app import mongodb_connection

import json

bp = Blueprint('taxi', __name__, url_prefix='/taxi')

@bp.route('/platform/list')
def taxi_platform_list():
    client = mongodb_connection()
    db = client['taxi']

    platform_list = list(db.taxi_platform.find())

    json_list = []
    for platform in platform_list:
        data = {
            'platform_id': str(platform['_id']),
            'platform_name': platform['platform_name']
        }
        json_list.append(data)
    print(json_list)
    return make_response(json.dumps(json_list, ensure_ascii=False))

