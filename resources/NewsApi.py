from flask_restful import Resource
from flask_restful import request
from configs.database import to_dict
from models.News import News
from models.Keyword import Keyword
from models.Secondary import news_keyword
from models.Site import Site


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

            all_news = News.query.filter(News.site_id == (i+1)).order_by(News.datetime.desc()).all()
            for j in range(len(all_news)):
                all_news[j] = to_dict(all_news[j])
            publishList[i]["all_news"] = all_news
        return {"publishList": publishList}, 200
