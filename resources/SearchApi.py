from flask_restful import Resource
from flask import request
from configs.database import to_dict
from models.News import News
from models.Keyword import Keyword
from models.Secondary import news_keyword
from models.Site import Site


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
        response = request.get_json()
        search_message = response["search_message"]
        search_item = {}
        try:
            result = News.query.filter(News.title == search_message).all()
            search_item["url"] = result[0].link
            search_item["status"] = 0
        except KeyError:
            search_item["status"] = 1
            return {"search_item": search_item}, 405
        return {"search_item": search_item}, 200
