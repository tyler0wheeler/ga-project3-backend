import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

post = Blueprint('posts', 'post')

@post.route('/', methods=["GET"])
def get_all_posts():
    try:
        posts = [model_to_dict(post) for post in models.Post.select()]
        print(posts)
        return jsonify(data=posts, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting this data"})

@post.route('/', methods=["POST"])
def create_posts():
    payload = request.get_json()
    print(type(payload), 'payload')
    post = models.Post.create(**payload)
    print(post.__dict__)
    print(dir(post))
    print(model_to_dict(post), 'model to dict')
    post_dict = model_to_dict(post)
    return jsonify(data=post_dict, status={"code": 201, "message": "Success"})
