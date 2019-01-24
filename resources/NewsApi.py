from flask_restful import Resource
from flask import request
from configs.database import to_dict, db
from models.News import News
from models.Site import Site
from models.Field import Field
from models.Keyword import Keyword
from resources.AuthApi import auth
from models.Secondary import news_field
from models.User import User
from datetime import datetime


class NewsApi(Resource):
    """
    :return news
    """
    @staticmethod
    def get():
        """
        optional arguments: status, site_id, limit
        :return: news ordered by sites in dict
        """
        args = request.args
        """
        try to receive the arguments
        """
        try:
            status = args["status"]
            a = 1
        except KeyError:
            a = 0
        try:
            site_id = args["site_id"]
            b = 2
        except KeyError:
            b = 0
        try:
            limit = args["limit"]
            c = 4
        except KeyError:
            c = 0
        try:
            date = args["date"]
            d = 100
        except KeyError:
            d = 0
        s = a + b + c + d

        if s == 0:
            publishList = Site.query.all()
            for item in range(len(publishList)):
                publishList[item] = to_dict(publishList[item])
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i + 1), News.status == 1) \
                    .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
                all_news_list = []
                for j in range(len(all_news_rows)):
                    all_news_dict = {
                        "id": all_news_rows[j].id,
                        "title": all_news_rows[j].title,
                        "link": all_news_rows[j].link,
                        "status": all_news_rows[j].status,
                        "click": all_news_rows[j].click,
                        "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "site_id": all_news_rows[j].site_id
                    }
                    all_news_list.append(all_news_dict)
                publishList[i]["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 1:
            publishList = Site.query.all()
            for item in range(len(publishList)):
                publishList[item] = to_dict(publishList[item])
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i + 1), News.status == status) \
                    .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
                all_news_list = []
                for j in range(len(all_news_rows)):
                    all_news_dict = {
                        "id": all_news_rows[j].id,
                        "title": all_news_rows[j].title,
                        "link": all_news_rows[j].link,
                        "status": all_news_rows[j].status,
                        "click": all_news_rows[j].click,
                        "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "site_id": all_news_rows[j].site_id
                    }
                    all_news_list.append(all_news_dict)
                publishList[i]["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 2:
            publishList = Site.query.filter(Site.id == site_id).first()
            publishList = to_dict(publishList)
            all_news_rows = News.query.filter(News.site_id == site_id, News.status == 1) \
                .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
            all_news_list = []
            for j in range(len(all_news_rows)):
                all_news_dict = {
                    "id": all_news_rows[j].id,
                    "title": all_news_rows[j].title,
                    "link": all_news_rows[j].link,
                    "status": all_news_rows[j].status,
                    "click": all_news_rows[j].click,
                    "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "site_id": all_news_rows[j].site_id
                }
                all_news_list.append(all_news_dict)
            publishList["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 4:
            publishList = Site.query.all()
            for item in range(len(publishList)):
                publishList[item] = to_dict(publishList[item])
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i + 1), News.status == 1) \
                    .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
                all_news_list = []
                for j in range(len(all_news_rows)):
                    all_news_dict = {
                        "id": all_news_rows[j].id,
                        "title": all_news_rows[j].title,
                        "link": all_news_rows[j].link,
                        "status": all_news_rows[j].status,
                        "click": all_news_rows[j].click,
                        "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "site_id": all_news_rows[j].site_id
                    }
                    all_news_list.append(all_news_dict)
                publishList[i]["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 3:
            publishList = Site.query.filter(Site.id == site_id).first()
            publishList = to_dict(publishList)
            all_news_rows = News.query.filter(News.site_id == site_id, News.status == status) \
                .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
            all_news_list = []
            for j in range(len(all_news_rows)):
                all_news_dict = {
                    "id": all_news_rows[j].id,
                    "title": all_news_rows[j].title,
                    "link": all_news_rows[j].link,
                    "status": all_news_rows[j].status,
                    "click": all_news_rows[j].click,
                    "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "site_id": all_news_rows[j].site_id
                }
                all_news_list.append(all_news_dict)
            publishList["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 5:
            publishList = Site.query.all()
            for item in range(len(publishList)):
                publishList[item] = to_dict(publishList[item])
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i + 1), News.status == status) \
                    .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
                all_news_list = []
                for j in range(len(all_news_rows)):
                    all_news_dict = {
                        "id": all_news_rows[j].id,
                        "title": all_news_rows[j].title,
                        "link": all_news_rows[j].link,
                        "status": all_news_rows[j].status,
                        "click": all_news_rows[j].click,
                        "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "site_id": all_news_rows[j].site_id
                    }
                    all_news_list.append(all_news_dict)
                publishList[i]["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 6:
            publishList = Site.query.filter(Site.id == site_id).first()
            publishList = to_dict(publishList)
            all_news_rows = News.query.filter(News.site_id == site_id, News.status == 1) \
                .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
            all_news_list = []
            for j in range(len(all_news_rows)):
                all_news_dict = {
                    "id": all_news_rows[j].id,
                    "title": all_news_rows[j].title,
                    "link": all_news_rows[j].link,
                    "status": all_news_rows[j].status,
                    "click": all_news_rows[j].click,
                    "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "site_id": all_news_rows[j].site_id
                }
                all_news_list.append(all_news_dict)
            publishList["all_news"] = all_news_list
            return {"publishList": publishList}, 200

        elif s == 100:
            today = datetime.now().strftime("%Y-%m-%d")
            publishList = Site.query.all()
            all_news = []
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i+1), News.status == 0, News.datetime > today) \
                    .order_by(News.datetime.desc(), News.id.desc()).all()
                for j in range(len(all_news_rows)):
                    news_backref = all_news_rows[j].fields.all()
                    if news_backref is not None:
                        for k in range(len(news_backref)):
                            news_backref[k] = news_backref[k].field
                    all_news_dict = {
                        "id": all_news_rows[j].id,
                        "title": all_news_rows[j].title,
                        "link": all_news_rows[j].link,
                        "status": all_news_rows[j].status,
                        "click": all_news_rows[j].click,
                        "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "site_id": all_news_rows[j].site_id,
                        "selectedFields": news_backref
                    }
                    all_news.append(all_news_dict)
            length = len(all_news)
            all_news = all_news[:10]
            return {"length": length, "publishList": all_news}, 200

        else:
            publishList = Site.query.filter(Site.id == site_id).first()
            publishList = to_dict(publishList)
            all_news_rows = News.query.filter(News.site_id == site_id, News.status == status) \
                .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
            all_news_list = []
            for j in range(len(all_news_rows)):
                news_backref = all_news_rows[j].fields.all()
                if news_backref is not None:
                    for i in range(len(news_backref)):
                        news_backref[i] = news_backref[i].field
                all_news_dict = {
                    "id": all_news_rows[j].id,
                    "title": all_news_rows[j].title,
                    "link": all_news_rows[j].link,
                    "status": all_news_rows[j].status,
                    "click": all_news_rows[j].click,
                    "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "site_id": all_news_rows[j].site_id,
                    "selectedFields": news_backref
                }
                all_news_list.append(all_news_dict)
            publishList["all_news"] = all_news_list
            return {"publishList": publishList}, 200

    @staticmethod
    def post():
        """
        get more news recording to the parmas
        :return: 10 new news in dirct sites
        """
        try:
            response = request.get_json()
            site_id = response["site_id"]
            news_id = response["news_id"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        more_news = News.query.filter(News.site_id == site_id, News.id < news_id, News.status == 1)\
            .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
        for i in range(len(more_news)):
            more_news[i] = to_dict(more_news[i])
        return {"more_news": more_news}, 200

    @auth.login_required
    def patch(self):
        """
        add fields to one direct news
        :return: success or error message
        """
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}
        try:
            response = request.get_json()
            news_id = response["news_id"]
            field_name_list = response["field_name_list"]
            news = News.query.filter(News.id == news_id).first()
            field = []
            for i in field_name_list:
                check_field = Field.query.filter(Field.field == i).first()
                if check_field is None:
                    return {"error": "please check the field list!"}, 403
                field.append(check_field)
            news.fields = field
            news.status = 1
            db.session.add(news)
            db.session.commit()
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        return {"message": "success"}, 201

    @auth.login_required
    def put(self):
        """
        change the news information
        :return: success or error message
        """
        response = request.get_json()
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}
        try:
            news_id = response["news_id"]
            news_title = response["title"]
            link = response["link"]
            site_id = response["site_id"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        news = News.query.filter(News.id == news_id).first()
        if news is None:
            return {"error": "there is no such news!"}, 403
        news.site_id = site_id
        news.link = link
        news.title = news_title
        db.session.commit()
        return {"message": "success"}, 201

    @auth.login_required
    def delete(self):
        """
        delete the user information in the database
        :return: success or error
        """
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}
        json = request.get_json()
        try:
            news = News.query.filter(News.id == json["news_id"]).first()
            if news is None:
                return {"error": "There is no such news"}, 403
            db.session.delete(news)
            db.session.commit()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        except AttributeError:
            return {"error": "Authorization denied"}, 401
        return {"status": "success", "message": "You have successfully deleted " + news.title + "!"}, 205
