from flask_restful import Resource
from flask import request
from configs.database import to_dict, db
from models.Site import Site
from models.User import User
from resources.AuthApi import auth


class SitedApi(Resource):
    """
    check and change the site information
    """
    @staticmethod
    def get():
        """
        get all the sites
        :return: dict
        """
        sites_list = Site.query.all()
        all_sites_list = []
        for j in range(len(sites_list)):
            all_sites_dict = {
                "id": sites_list[j].id,
                "name": sites_list[j].name
            }
            all_sites_list.append(all_sites_dict)
        return {"sites_list": all_sites_list}, 200
