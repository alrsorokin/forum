from datetime import datetime

from flask import abort, g, jsonify, request, make_response
from flask.views import MethodView
from flask_expects_json import expects_json
from sqlalchemy.exc import DatabaseError

from forum.models import Section
from forum.lib.validators import validate_section
from . import schemas


class SectionListView(MethodView):
    def get(self):
        sections = Section.query.all()
        return make_response(jsonify([section.json() for section in sections]), 200)

    @expects_json(schemas.section)
    def post(self):
        try:
            section = Section(theme=g.data['theme'],
                              description=g.data['description'],
                              created_at=datetime.now()).save()
        except DatabaseError:
            abort(400)

        return make_response(jsonify(section.json()), 201)


class SectionView(MethodView):

    decorators = [validate_section]

    def get(self, section):
        return make_response(jsonify(section.json()), 200)

    def delete(self, section):
        section.delete()
        return make_response(jsonify("Deleted"), 204)

    @expects_json(schemas.section)
    def put(self, section):
        try:
            section.update(theme=g.data['theme'],
                           description=g.data['description'],
                           updated_at=datetime.now())
        except DatabaseError:
            abort(400)

        return make_response(jsonify(section.json()), 202)
