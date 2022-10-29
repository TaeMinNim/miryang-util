from flask import Blueprint, make_response,g ,request,jsonify
from app import mongodb_connection
from pymongo import ReturnDocument
from datetime import datetime
from bson import ObjectId
import json

bp = Blueprint('taxi', __name__, url_prefix='/taxi')

@bp.route('/platform/list')
def taxi_platform_list():
    if not g.user_id:
        return ('access denied', 500)
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

@bp.route('/post/posting', methods=['POST'])
def delivery_posting():
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    mongo_db = client['taxi']

    json = request.get_json()

    today = datetime.now()
    data = {
        'user_id': g.user_id,
        'join_user': [g.user_id],
        'nick_name': g.nick_name,
        'title': json['title'],
        'content': json['content'],
        'depart_time': json['depart_time'],
        'depart_name': json['depart_name'],
        'dest_name': json['dest_name'],
        'min_member': json['min_member'],
        'max_member': json['max_member'],
        'update_date': today.strftime('%Y-%m-%dT%H:%M:%S'),
        'views': 0,
        'is_closed': False,
    }

    print(data)

    _id = mongo_db.taxi_post.insert_one(data)
    post_id = str(_id.inserted_id)

    return jsonify(post_id=post_id, success=True)

@bp.route('/post/detail/<string:post_id>')
def taxi_post_detail(post_id):
    if not g.user_id:
        return ('access denied', 500)

    client = mongodb_connection()
    db = client['taxi']

    find = {
        '_id': ObjectId(post_id)
    }
    update = {
        '$inc': { 'views': 1 }
    }

    post = db.taxi_post.find_one_and_update(find, update, return_document=ReturnDocument.AFTER)
    print(post)
    post['_id'] = str(post['_id'])

    return make_response(json.dumps(post, ensure_ascii=False))

@bp.route('/post/condition-switch', methods=['PATCH'])
def taxi_post_condition_switch():
    json = request.get_json()
    post_id = json['post_id']

    client = mongodb_connection()
    db = client['taxi']

    find = {
        '_id': ObjectId(post_id)
    }
    post = db.taxi_post.find_one(find)

    update = {
        '$set': { 'is_closed' : not post['is_closed'] }
    }
    db.taxi_post.update_one(find, update)

    return jsonify(post_id=post_id, success=True, condition= not post['is_closed'])

@bp.route('/post/join/condition-switch', methods=['PATCH'])
def taxi_post_join():
    if not g.user_id:
        return ('access denied', 500)
    client = mongodb_connection()
    db = client['taxi']
    json = request.get_json()
    post_id = json['post_id']
    find = {
        '_id': ObjectId(post_id)
    }
    post = db.taxi_post.find_one(find)

    if g.user_id == post['user_id']:
        return ('대표자는 그룹을 탈퇴할 수 없습니다', 500)

    if g.user_id in post['join_user']:
        joined = False
        update = {
            '$pull': {
                'join_user': g.user_id,
            }

        }
    else:
        joined=True
        update = {
            '$push': {
                'join_user': g.user_id
            }

        }
    db.taxi_post.update_one(find, update)

    return jsonify(post_id=post_id, success=True, join=joined)

@bp.route('/post/list')
def taxi_post_list():
    if not g.user_id:
        return ('access denied', 500)
    client = mongodb_connection()
    db = client['taxi']

    projection = {
        'content': False,
    }
    post_list = list(db.taxi_post.find({}, projection))
    for post in post_list:
        post['_id'] = str(post['_id'])
    return make_response(json.dumps(post_list, ensure_ascii=False))