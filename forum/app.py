from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.after_request
def session_commit(response):
    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        db.session.remove()
        raise

    return response


from forum.api.v1 import urls  # isort:skip
