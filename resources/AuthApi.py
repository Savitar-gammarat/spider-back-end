from flask import request, g
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource
from models.User import User
from configs.database import to_dict, db
from datetime import datetime

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    """
    Verify the token
    :param token: given token
    :return: bool
    """
    g.current_user = User.verify_token(token)
    return g.current_user is not None


class AuthAPI(Resource):
    """
    Authorization API
    """
    @staticmethod
    def post():
        """
        Login in
        :return: token or error message
        """
        try:
            username = request.json.get("username")
            password = request.json.get("password")
        except KeyError:
            return {"error": "lack necessary arguments!"}, 406
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"error": "Username doesn't exist"}, 404
        if not user.verify_password(password):
            return {"error": "Wrong password"}, 403
        user.last_login_time = datetime.now()
        db.session.commit()
        token = user.generate_auth_token()
        user = to_dict(user)
        if user["customization"] is None:
            return {
                "token": token,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                }
            }, 201
        return {
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "customization": user["customization"]
            }
        }, 201
