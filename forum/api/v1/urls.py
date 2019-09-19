from flask import jsonify, make_response

from forum.app import app
from forum.lib.const import ERRORS

from .section import SectionListView, SectionView
from .comments import CommentView
from .post import PostListView, PostView


@app.route('/api/v1/health-check', methods=['GET'])
def health_check():
    from forum.models import Section
    Section.query.first()
    return 'OK'


@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify(ERRORS[404]), 404)


@app.errorhandler(400)
def error_400(error):
    return make_response(jsonify(ERRORS[400]), 400)


app.add_url_rule('/api/v1/sections', view_func=SectionListView.as_view('section_list'))
app.add_url_rule('/api/v1/sections/<section_id>', view_func=SectionView.as_view('section'))

app.add_url_rule('/api/v1/sections/<section_id>/posts', view_func=PostListView.as_view('post_list'))
app.add_url_rule('/api/v1/sections/<section_id>/posts/<post_id>',
                 view_func=PostView.as_view('post'))

app.add_url_rule('/api/v1/sections/<section_id>/posts/<post_id>/comments',
                 view_func=CommentView.as_view('comment'))
