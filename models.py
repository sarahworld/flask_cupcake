"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    flavor = db.Column(db.String(100), nullable=False)

    size = db.Column(db.String(100), nullable=False)

    rating = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(1000), nullable=False, default='https://tinyurl.com/demo-cupcake')

    def serialize_cupcake(cupcake):
        return {
                'id':cupcake.id,
                 'flavor':cupcake.flavor,
                 'size':cupcake.size,
                 'rating':cupcake.rating,
                 'image':cupcake.image
                 }


