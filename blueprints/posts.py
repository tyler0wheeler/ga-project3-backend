import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

from flask_login import login_required

post = Blueprint('posts', 'post')

@post.route('/', methods=["GET"])
def get_all_posts():
    try:
        posts = [model_to_dict(post) for post in models.Post.select()]
        likes = [model_to_dict(like) for like in models.Likes.select()]
        return jsonify(data={"posts":posts, "likes":likes}, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting this data"})


@post.route('/', methods=["POST"])
@login_required
def create_posts():
    payload = request.get_json()
    new_user_post = models.Post.create(title=payload['title'], img=payload['img'], description=payload['description'], owner=current_user.id, tags=payload['tags'])
    post_dict = model_to_dict(new_user_post)
    return jsonify(data=post_dict, status={"code": 200, "message": "Success"})

@post.route('/<id>', methods=["GET"])
def get_one_post(id):
    post = models.Post.get_by_id(id)
    return jsonify(data=model_to_dict(post), status={"code": 200, "message": "Success"})

@post.route('/userposts/', methods=["GET"])
@login_required
def get_one_user():
    likes = [model_to_dict(like) for like in models.Likes.select()]
    posts = [model_to_dict(post) for post in current_user.posts]
    return jsonify(data={"posts":posts, "likes":likes}, status={"code": 200, "message": "Success"})

@post.route('/<id>', methods=["PUT"])
@login_required
def update_post(id):
    payload = request.get_json()
    query = models.Post.update(**payload).where(models.Post.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Post.get_by_id(id)), status={"code": 200, "message": "Success"})

@post.route('/<id>', methods=["DELETE"])
@login_required
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id==id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="Successfully deleted {} post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )

@post.route('/like/<post_id>', methods=["POST"])
@login_required
def create_like(post_id):
    liked_post_id = post_id
    user_that_liked = current_user.id
    new_like = models.Likes.create(post=liked_post_id, user=user_that_liked)
    like_dict = model_to_dict(new_like)
    return jsonify(data=like_dict, status={"code": 200, "message": "Success"})

@post.route('/delete/<post_id>', methods=["DELETE"])
@login_required
def delete_like(post_id):
    delete_like_query = models.Likes.delete().where((models.Likes.post==post_id) & (models.Likes.user_id==current_user.id))
    num_of_rows_like_deleted = delete_like_query.execute()
    return jsonify(
    data={},
    message="Successfully deleted {} like with id {}".format(num_of_rows_like_deleted, post_id),
    status={"code": 200}
    )
@post.route('/delete-all-likes/<post_id>', methods=["DELETE"])
@login_required
def delete_all_likes(post_id):
    delete_all_likes_query= models.Likes.delete().where(models.Likes.post_id==post_id)
    num_of_rows_likes_deleted = delete_all_likes_query.execute()
    return jsonify(data={}, message="Successfully deleted {} likes with id {}".format(num_of_rows_likes_deleted, post_id), status={"code":200}) 