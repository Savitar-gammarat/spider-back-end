from flask_restful import Resource
# from flask_restful import request
from configs.database import to_dict
from models.News import News
from models.Site import Site
from models.Field import Field
from models.Keyword import Keyword


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
            all_news_rows = News.query.filter(News.site_id == (i+1)).order_by(News.datetime.desc()).limit(20).all()
            all_news_list = []
            for j in range(len(all_news_rows)):
                all_news_dict = {}
                all_news_dict["id"] = all_news_rows[j].id
                all_news_dict["title"] = all_news_rows[j].title
                all_news_dict["link"] = all_news_rows[j].link
                all_news_dict["datetime"] = all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S")
                all_news_dict["site_id"] = all_news_rows[j].site_id
                all_news_list.append(all_news_dict)
            publishList[i]["all_news"] = all_news_list
        return {"publishList": publishList}, 200
