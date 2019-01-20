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
        optional arguments: status, site_id
        get all the news ordered by sites
        :return: news ordered by sites in dict
        """
        args = request.args
        # 没有参数的情况，默认遍历所有站点下的status为1的新闻，默认20条
        if len(args) == 0:
            publishList = Site.query.all()
            for item in range(len(publishList)):
                publishList[item] = to_dict(publishList[item])
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i+1), News.status == 1)\
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
        # 有参数的情况
        if len(args) > 0:
            # 有status的情况
            if "status" in args:
                status = args["status"]
                # 有status和site_id的情况
                if "site_id" in args:
                    site_id = args["site_id"]
                    # 有status，site_id和limit参数的情况
                    if "limit" in args:
                        limit = args["limit"]
                        all_news_rows = News.query.filter(News.site_id == site_id, News.status == status)\
                            .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
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
                        return {"publishList": all_news_list}, 200
                    # 有status，site_id，没有limit参数的情况， 默认为10条新闻
                    all_news_rows = News.query.filter(News.site_id == site_id, News.status == status) \
                        .order_by(News.datetime.desc(), News.id.desc()).limit(10).all()
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
                    return {"publishList": all_news_list}, 200
                # 有status,没有site_id,有limit的情况
                if "limit" in args:
                    limit = args["limit"]
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
                                "datetime": all_news_rows[j].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                "site_id": all_news_rows[j].site_id
                            }
                            all_news_list.append(all_news_dict)
                        publishList[i]["all_news"] = all_news_list
                    return {"publishList": publishList}, 200
                # 有status,没有site_id和limit的情况，默认10条新闻
                publishList = Site.query.all()
                for item in range(len(publishList)):
                    publishList[item] = to_dict(publishList[item])
                for i in range(len(publishList)):
                    all_news_rows = News.query.filter(News.site_id == (i + 1), News.status == status) \
                        .order_by(News.datetime.desc(), News.id.desc()).limit(10).all()
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
            # 没有status,有site_id, limit的情况，默认0
            if "site_id" in args:
                site_id = args["site_id"]
                if "limit" in args:
                    limit = args["limit"]
                    all_news_rows = News.query.filter(News.site_id == site_id, News.status == 0) \
                        .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
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
                    return {"publishList": all_news_list}, 200
                # 没有status,有site_id, 没有limit的情况
                all_news_rows = News.query.filter(News.site_id == site_id, News.status == 0) \
                    .order_by(News.datetime.desc(), News.id.desc()).limit(10).all()
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
                return {"publishList": all_news_list}, 200
            # 没有status, 没有site_id, 有limit的情况
            limit = args["limit"]
            publishList = Site.query.all()
            for item in range(len(publishList)):
                publishList[item] = to_dict(publishList[item])
            for i in range(len(publishList)):
                all_news_rows = News.query.filter(News.site_id == (i + 1), News.status == 0) \
                    .order_by(News.datetime.desc(), News.id.desc()).limit(limit).all()
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
            return {"error": "lack necessary argument!"}, 406
        more_news = News.query.filter(News.site_id == site_id, News.id < news_id, News.status == 1)\
            .order_by(News.datetime.desc(), News.id.desc()).limit(20).all()
        for i in range(len(more_news)):
            more_news[i] = to_dict(more_news[i])
        return {"more_news": more_news}, 200
    #
    # @auth.login_required
    # def patch(self):
    #     """
    #     add fields to one direct news
    #     :return: success or error message
    #     """
    #     try:
    #         response = request.get_json()
    #         for i in range(len(response)):
    #             response[i] = response["site_id"]
    #
    #     except KeyError:
    #         return {"error": "lack necessary argument!"}