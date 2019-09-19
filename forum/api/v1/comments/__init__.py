from datetime import datetime

from flask import abort, g, jsonify, request, make_response
from flask.views import MethodView
from flask_expects_json import expects_json
from sqlalchemy.exc import DatabaseError

from forum.models import Comment
from forum.lib.validators import validate_post
from . import schemas


class CommentView(MethodView):

    decorators = [validate_post]

    @expects_json(schemas.comment)
    def post(self, post):
        try:
            comment = Comment(text=g.data['text'],
                              created_at=datetime.now(),
                              post=post).save()
        except DatabaseError:
            abort(400)

        return make_response(jsonify(comment.json()), 201)
