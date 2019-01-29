from flask_restful import Resource
from flask import request
from configs.database import to_dict
from models.News import News
from models.Site import Site
from resources.maintenance.AuthApi import auth
from models.User import User


class SearchApi(Resource):
    """
    :return news_list
    """
    @staticmethod
    def get():
        """
        get all the news
        :return: news in dict
        """
        news_list = News.query.all()
        site_list = Site.query.all()
        for item in range(len(news_list)):
            news_list[item] = to_dict(news_list[item])
        for site in range(len(site_list)):
            site_list[site] = to_dict(site_list[site])
        search_message_list = []
        for i in range(len(news_list)):
            for number in range(len(site_list)):
                if news_list[i]["site_id"] == number+1:
                    news_list[i]["site_name"] = site_list[number]["name"]
            search_message_list.append(news_list[i]["site_name"] + ":" +
                                       news_list[i]["title"])
        return {"search_message_list": search_message_list}, 200

    @staticmethod
    def post():
        """
        get the specific news' url
        :return: news' url
        """
        search_item = {}
        try:
            response = request.get_json()
            search_message = response["search_message"]
            result = News.query.filter(News.title == search_message).all()
            search_item["url"] = result[0].link
            search_item["status"] = 0
        except KeyError:
            return {"error": "lack necessary key"}, 406
        except IndexError:
            search_item["status"] = 1
            return {
                       "error": "there is no such news in database",
                       "search_item": search_item
                   }, 406
        return {"search_item": search_item}, 200

    @auth.login_required
    def put(self):
        """
        search the news by id
        :return: news or change news
        """
        if not User.is_super_admin():
            return {"error": "you have no rights to do that!"}, 401
        try:
            response = request.get_json()
            news_id = response["news_id"]
        except KeyError:
            return {"error": "lack necessary key"}, 406
        news = News.query.filter(News.id == news_id).first()
        if news is None:
            return {"error": "there is no such news"}, 403
        news_backref = news.fields.all()
        if news_backref is not None:
            for i in range(len(news_backref)):
                news_backref[i] = news_backref[i].field
        all_news_dict = {
            "id": news.id,
            "title": news.title,
            "link": news.link,
            "status": news.status,
            "click": news.click,
            "datetime": news.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "site_id": news.site_id,
            "selectedFields": news_backref
        }
        return {"publishList": [all_news_dict]}, 201
