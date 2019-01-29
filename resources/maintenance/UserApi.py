from flask_restful import Resource
from flask import request, g
from configs.database import db
from models.User import User
from datetime import datetime
from resources.maintenance.AuthApi import auth


class UserApi(Resource):
    """
    change or query user information
    """

    @staticmethod
    def get():
        """
        get the user information
        :return: success or error message
        """
        counts = User.query.count()
        return {"counts": counts}, 200

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

    @auth.login_required
    def patch(self):
        """
        change the password
        :return: user information or error message
        """
        json = request.get_json()
        try:
            username = json["username"]
            password = json["password"]
            user = User.query.filter(User.username == username).first()
            if not User.is_super_admin():
                if not g.current_user.id == user.id:
                    return {"error": "you have no rights to do that!"}, 401
            user.hash_password(password)
            db.session.commit()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        return {"status": "success"}, 201

    @auth.login_required
    def put(self):
        """
        change the customization
        :return: user information or error message
        """
        json = request.get_json()
        try:
            username = json["username"]
            customization = json["customization"]
            user = User.query.filter(User.username == username).first()
            if not User.is_super_admin():
                if not g.current_user.id == user.id:
                    return {"error": "you have no rights to do that!"}, 401
            user.customization = customization
            db.session.commit()
            user = User.query.filter(User.username == username).first()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        return {
                    "status": "success",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "customization": user.customization
                    }
               }, 201

    @auth.login_required
    def delete(self):
        """
        delete the user information in the database
        :return: success or error
        """
        json = request.get_json()
        try:
            if not User.is_super_admin():
                return {"error": "you have no rights to do that!"}, 401
            user = User.query.filter(User.username == json["username"]).first()
            if user is None:
                return {"error": "There is no such username"}, 403
            db.session.delete(user)
            db.session.commit()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        except AttributeError:
            return {"error": "Authorization denied"}, 401
        return {"status": "success", "message": "You have successfully deleted " + user.username + "!"}, 205

