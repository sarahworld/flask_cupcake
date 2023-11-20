"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Its a secret';
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/api/cupcakes')
def all_cupcakes():
    all_cupcakes = Cupcake.query.all();
    serialized = [Cupcake.serialize_cupcake(each) for each in all_cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_detail(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id);
    serialized = Cupcake.serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image','https://tinyurl.com/demo-cupcake')

    new_cupcake = Cupcake(flavor=flavor,size=size, rating=rating,image=image);
    db.session.add(new_cupcake);
    db.session.commit();

    serialized = Cupcake.serialize_cupcake(new_cupcake);
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake_to_edit = Cupcake.query.get_or_404(cupcake_id);

    cupcake_to_edit.flavor = request.json['flavor']
    cupcake_to_edit.size = request.json['size']
    cupcake_to_edit.rating = request.json['rating']
    cupcake_to_edit.image = request.json.get('image')

    db.session.add(cupcake_to_edit);
    db.session.commit();

    serialized = Cupcake.serialize_cupcake(cupcake_to_edit);
    return (jsonify(cupcake=serialized))


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake_to_delete = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake_to_delete)
    db.session.commit();

    return (jsonify(message="Deleted"))

