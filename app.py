from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from configs.config import (DB_HOST, DB_PORT, DB_SCHEMA, DB_USER, DB_PASSWORD)
from configs.database import db
from resources.NewsApi import NewsApi
from resources.SearchApi import SearchApi
from resources.UserApi import UserApi
from resources.AuthApi import AuthAPI
from resources.FieldApi import FieldApi


app = Flask(__name__)
CORS(app)
api = Api(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = \
#     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:991004@47.101.196.53:3306/news-aggregation"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


with app.app_context():
    db.init_app(app)    # init db
    db.create_all()     # create tables

api.add_resource(NewsApi, '/api/v0/news')
api.add_resource(SearchApi, '/api/v0/search')
api.add_resource(UserApi, '/api/v0/user')
api.add_resource(AuthAPI, '/api/v0/auth')
api.add_resource(FieldApi, '/api/v0/field')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
