# app.py
import json

from flask import Flask, request
from flask_restx import Api, Resource

from marshmallow import Schema, fields

from config import app, db
from models import Movie
from schemas import MovieSchema

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route("/")
class MoviesViews(Resource):
    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        query = Movie.query
        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        return MovieSchema(many=True).dump(query.all()), 200

    def post(self):
        data = request.json
        try:
            db.session.add(
                Movie(**data)
            )
            db.session.commit()
            return "Успех", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неуспешно", 500


@movie_ns.route("/<int:id>/")
class MoviesViews(Resource):
    def get(self, id):
        result = db.session.query(Movie).filter(Movie.id == id).all()

        Movie.query.filter(Movie.id == id)

        if len(result):
            return MovieSchema().dump(result), 200
        else:
            return json.dumps({}), 200

    def put(self, id):
        data = request.json
        try:
            result = Movie.query.filter(Movie.id == id).one()
            result.title = data.get('title')
            db.session.add(result)
            db.session.commit()
            return "Обновились", 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Необновилось", 200

    def __delete(self, id):
        try:
            result = Movie.query.filter(Movie.id == id).one()
            db.session.delete(result)
            db.session.commit()
            return "Удалилй", 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Не удалилй", 200


if __name__ == '__main__':
    app.run(port=8081, debug=True)
