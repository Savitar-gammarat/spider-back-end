from flask_restful import Resource
from flask import request
from configs.database import db
from models.User import User
from datetime import datetime


class UserApi(Resource):
    """
    change or query user information
    """
    @staticmethod
    def post():
        """
        Register
        :return: success or error message
        """
        json = request.get_json()
        try:
            user = User(
                username=json["username"],
                email=json["email"],
                create_time=datetime.now()
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        if User.query.filter_by(username=user.username).first() is not None:
            return {"error": "User name has already been taken."}, 403
        user.hash_password(json["password"])
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=user.username).first()
        token = user.generate_auth_token()
        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, 201

    @staticmethod
    def patch():
        """
        change the password
        :return: user information or error message
        """
        pass

    @staticmethod
    def put():
        """
        change the customization
        :return: user information or error message
        """
        pass

    @staticmethod
    def delete():
        """
        delete the user information in the database
        :return: success or error
        """
        pass
