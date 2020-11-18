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
    return jsonify(data=post_dict, status={"code": 200, "message": "Success"})

@post.route('/<id>', methods=["GET"])
def get_one_post(id):
    # print(id, 'reserved word')
    post = models.Post.get_by_id(id)
    return jsonify(data=model_to_dict(post), status={"code": 200, "message": "Success"})

@post.route('/<id>', methods=["PUT"])
def update_post(id):
    payload = request.get_json()
    # print(payload)
    query = models.Post.update(**payload).where(models.Post.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Post.get_by_id(id)), status={"code": 200, "message": "Success"})

@post.route('/<id>', methods=["DELETE"])
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)
    # write logic -- if you have no rows deleted you will proabbly want some message telling you so
    return jsonify(
    data={},
    message="Successfully deleted {} post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )
