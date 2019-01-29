from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_compress import Compress
from configs.config import (DB_HOST, DB_PORT, DB_SCHEMA, DB_USER, DB_PASSWORD)
from configs.database import db
from resources.maintenance.NewsApi import NewsApi
from resources.maintenance.SearchApi import SearchApi
from resources.maintenance.UserApi import UserApi
from resources.maintenance.AuthApi import AuthAPI
from resources.maintenance.FieldApi import FieldApi
from resources.maintenance.CountApi import CounterApi
from resources.maintenance.SiteApi import SitedApi
from resources.test import Test
from resources.analysis.LoginAnalysisApi import LoginAnalysisApi
from resources.analysis.FieldAnalysisApi import FieldAnalysisApi


app = Flask(__name__)
CORS(app)
Compress(app)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
"""
    something important！ Please use Python 3.7+
    If you are using python 2.0+, please use the under config
"""
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:991004@47.101.196.53:3306/news-aggregation"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


with app.app_context():
    db.init_app(app)    # init db
    db.create_all()     # create tables

api.add_resource(NewsApi, '/api/v0/news')
api.add_resource(SearchApi, '/api/v0/search')
api.add_resource(UserApi, '/api/v0/user')
api.add_resource(AuthAPI, '/api/v0/auth')
api.add_resource(FieldApi, '/api/v0/field')
api.add_resource(CounterApi, '/api/v0/counter')
api.add_resource(SitedApi, '/api/v0/site')
api.add_resource(LoginAnalysisApi, '/api/v0/loginanalysis')
api.add_resource(Test, '/api/v0/test')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
