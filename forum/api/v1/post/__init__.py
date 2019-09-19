from datetime import datetime

from flask import abort, g, jsonify, request, make_response
from flask.views import MethodView
from flask_expects_json import expects_json
from sqlalchemy.exc import DatabaseError

from forum.models import Post
from forum.lib.validators import validate_section, validate_post

from . import schemas


class PostListView(MethodView):

    decorators = [validate_section]

    def get(self, section):
        return make_response(jsonify([post.json() for post in section.posts]), 200)

    @expects_json(schemas.post)
    def post(self, section):
        try:
            post = Post(theme=g.data['theme'],
                        description=g.data['description'],
                        created_at=datetime.now(),
                        section=section).save()
        except DatabaseError:
            abort(400)

        return make_response(jsonify(post.json()), 201)


class PostView(MethodView):

    decorators = [validate_post]

    def get(self, post):
        return make_response(jsonify(post.json(extended=True)), 200)

    def delete(self, post):
        post.delete()
        return make_response(jsonify("Deleted"), 204)

    @expects_json(schemas.post)
    def put(self, post):
        try:
            post.update(theme=g.data['theme'],
                        description=g.data['description'],
                        section_id=post.section_id,
                        updated_at=datetime.now())
        except DatabaseError:
            abort(400)

        return make_response(jsonify(post.json()), 202)
