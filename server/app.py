#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return 'hello'

class Campers(Resource):
    def get(self):
        #import ipdb; ipdb.set_trace()
        # campers = [ campers.to_dict(rules=('-signups_c', )) for campers in Camper.query.all()]
        campers = [ camper.to_dict(only=("id", "name", "age", )) for camper in Camper.query.all()]

        return make_response(campers, 200)
    
    def post(self):
        try:
            new_camper = Camper(
                name = request.json['name'],
                age = request.json['age']
            )
            db.session.add(new_camper)
            db.session.commit()

            return new_camper.to_dict(rules = ('-signups_c', )), 201
        except ValueError:
            return make_response({
                "ERROR": ["validation error"]
            }, 400)

api.add_resource(Campers, "/campers")


class CampersById(Resource):
    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).one_or_none()

        if camper is None:
            return make_response({'error': 'Camper not found'}, 404)
        
        return make_response(camper.to_dict(), 200)
    
    def patch(self, id):
        camper = Camper.query.filter(Camper.id == id).one_or_none()

        if camper is None:
            return {'error': 'camper not found'}, 404
        
        request_json = request.get_json()

        try: 
            setattr(camper, 'name', request_json['name'])
            setattr(camper, 'age', request_json['age'])

            db.session.add(camper)
            db.session.commit()

            return camper.to_dict(rules=()), 202

        except ValueError:
            return make_response({"errors": ["validation error"]}, 400)

api.add_resource(CampersById, "/campers/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)