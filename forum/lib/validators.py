from flask import abort

from forum.models import Section, Post, Comment


def validate_section(f):
    def validate(section_id):
        section = Section.query.get(section_id)
        if not section:
            abort(404)

        return f(section=section)
    return validate


def validate_post(f):
    def validate(section_id, post_id):
        section = Section.query.get(section_id)
        post = Post.query.get(post_id)
        if not post or not section:
            abort(404)

        return f(post=post)
    return validate
