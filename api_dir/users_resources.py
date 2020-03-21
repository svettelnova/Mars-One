from flask_restful import abort, Resource, Api, reqparse
from flask import jsonify
from data import db_session
from data.users import User
from api_dir.pars import *


def abort_if_job_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_already_exists(email):
    session = db_session.create_session()
    if session.query(User).find(User.email == email).exists():
        abort(409, message=f"User {email} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_job_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})

    def delete(self, user_id):
        abort_if_job_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser.parse_args()
        abort_if_job_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.surname = args['surname']
        user.name = args['name']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.hashed_password = args['hashed_password']


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password')) for item
            in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if not user:
            return jsonify({'error': 'Not found'})
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})
