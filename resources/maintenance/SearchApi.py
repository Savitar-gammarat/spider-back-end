from flask_restful import Resource
from flask import request
from configs.database import to_dict
from models.News import News
from models.Site import Site
from resources.maintenance.AuthApi import auth
from models.User import User
import jieba
import re


class SearchApi(Resource):
    """
    :return news_list
    """
    @staticmethod
    def get():
        try:
            args = request.args
            seg = args["seg"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        seg_list = jieba.cut(seg, cut_all=False)
        msg_list = []
        result_list = []
        for seg in seg_list:
            msg_list.append(seg)
        all_news = News.latest_news()
        for i in range(len(all_news)):
            for j in range(len(msg_list)):
                status = re.match(msg_list[j], all_news[i].title)
                if status is not None:
                    result_list.append({
                        "id": all_news[i].id,
                        "title": all_news[i].title,
                        "link": all_news[i].link,
                        "click": all_news[i].click,
                        "datetime": all_news[i].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "site_id": all_news[i].site_id,
                    })
                    break
        return {"all_news": result_list}, 200

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
