from flask_restful import Resource
from flask import request
from configs.database import to_dict
from models.News import News
from models.Site import Site
from models.Field import Field
from models.Keyword import Keyword
from resources.AuthApi import auth


class NewsApi(Resource):
    """
    :return news
    """
    @staticmethod
    def get():
        """
        get all the news ordered by sites
        :return: news ordered by sites in dict
        """

        publishList = Site.query.all()
        for item in range(len(publishList)):
            publishList[item] = to_dict(publishList[item])
        for i in range(len(publishList)):
            all_news_rows = News.query.filter(News.site_id == (i+1))\
                .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
            all_news_list = []
            for j in range(len(all_news_rows)):
                all_news_dict = {
                    "id": all_news_rows[j].id,
                    "title": all_news_rows[j].title,
                    "link": all_news_rows[j].link,
                    "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "site_id": all_news_rows[j].site_id
                }
                all_news_list.append(all_news_dict)
            publishList[i]["all_news"] = all_news_list
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
            return {"error": "parmas error"}, 405
        more_news = News.query.filter(News.site_id == site_id, News.id < news_id)\
            .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
        for i in range(len(more_news)):
            more_news[i] = to_dict(more_news[i])
        return {"more_news": more_news}, 200
