from resources.maintenance.AuthApi import auth
from models.User import User
from flask_restful import Resource


class Test(Resource):
    @auth.login_required
    def get(self):
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}
        return {"message": "success"}, 201
