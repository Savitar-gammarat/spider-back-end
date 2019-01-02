from flask_restful import Resource
from flask_restful import request
from configs.database import to_dict
from models.News import News
from models.Keyword import Keyword
from models.Secondary import news_keyword
from models.Site import Site


class NewsApi(Resource):
    """
    :return
    """
    @staticmethod
    def get():
        """

        :return:
        """
        all_news = News.query.order_by(News.datetime.desc()).all()
        print(all_news)
        for i in range(len(all_news)):
            all_news[i] = to_dict(all_news[i])
        print(all_news)
        return {"all_news": all_news}, 200
