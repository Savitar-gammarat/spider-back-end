from flask_restful import Resource
from flask import request
from configs.database import to_dict, db
from models.Field import Field
from models.User import User
from resources.maintenance.AuthApi import auth


class FieldApi(Resource):
    """
    check and change the field information
    """
    @staticmethod
    def get():
        """
        get all the fields
        :return: dict
        """
        fields_list = Field.query.all()
        for i in range(len(fields_list)):
            fields_list[i] = to_dict(fields_list[i])
        return {"fields_list": fields_list}, 200

    @auth.login_required
    def patch(self):
        """
        check the fields
        :return: success or error message
        """
        response = request.get_json()
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}, 401
        try:
            field_id = response["field_id"]
            field_name = response["field_name"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        field = Field.query.filter(Field.id == field_id).first()
        if field is None:
            return {"error": "there is no such field"}, 403
        output = field.field
        field.field = field_name
        db.session.commit()
        return {"message": "you have successfully change the " + output + " into " + field_name}

    @auth.login_required
    def put(self):
        """
        add new field
        :return: success or error message
        """
        response = request.get_json()
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}, 401
        try:
            field_name = response["field_name"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        field = Field.query.filter(Field.field == field_name).first()
        if field is not None:
            return {"error": "there already has such field"}, 403
        field = Field(
            field=field_name
        )
        db.session.add(field)
        db.session.commit()
        return {"message": "you have successfully change the " + field_name}, 201

    @auth.login_required
    def delete(self):
        """
        delete the field information in the database
        :return: success or error message
        """
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}, 401
        json = request.get_json()
        try:
            field = Field.query.filter(Field.id == json["field_id"]).first()
            if field is None:
                return {"error": "There is no such news"}, 403
            db.session.delete(field)
            db.session.commit()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        except AttributeError:
            return {"error": "Authorization denied"}, 401
        return {"status": "success", "message": "You have successfully deleted " + field.field + "!"}, 205
