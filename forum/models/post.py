from forum.app import db

from . import Base


class Post(Base):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def jsonify(self, res):
        res['comments'] = [comment.json() for comment in self.comments]
