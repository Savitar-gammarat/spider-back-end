from flask_restful import Resource
from flask import request
from configs.database import to_dict, db
from models.Field import Field
from models.User import User
from resources.AuthApi import auth


class FieldApi(Resource):
    """
    check and change the field information
    """
    @auth.login_required
    def get(self):
        """
        get all the fields
        :return: dict
        """
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}
        fields_list = Field.query.all()
        for i in range(len(fields_list)):
            fields_list[i] = to_dict(fields_list[i])
        return {"fields_list": fields_list}, 200

    @staticmethod
    def patch():
        """
        check the fields
        :return: success or error message
        """

        response = request.get_json()
        try:
            field_id = response["field_id"]
            field_name = response["field_name"]
        except KeyError:
            return {"error": "there is no such field!"}, 403
        field = Field.query.filter(Field.id == field_id).first()
        if field is None:
            return {"error": "there is no such field"}, 403
        output = field.field
        field.field = field_name
        db.session.commit()
        return {"message": "you have successfully change the " + output + "into " + field_name}

    @staticmethod
    def put():
        """
        add new field
        :return: success or error message
        """

