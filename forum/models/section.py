from forum.app import db

from . import Base


class Section(Base):

    __tablename__ = 'section'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='section', lazy=True)
