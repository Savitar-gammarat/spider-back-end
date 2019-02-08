from flask_restful import Resource
from models.Keyword import Keyword
from models.Counter import Counter
from datetime import datetime, timedelta
from configs.database import db, to_dict
from models.Site import Site
from models.News import News
from configs.config import cache
from flask import request


class KeywordsAnalysisApi(Resource):
    @staticmethod
    # @cache.cached(timeout=600)
    def post():
        try:
            site_id = request.get_json()["site_id"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        keywords_news_list = []
        time_list = []
        keywords_list = []
        data_list =[]
        time_a = datetime.now()
        time_b = time_a - timedelta(days=7)
        keywords = Keyword.query.filter(Keyword.datetime > time_b).all()
        for i in range(len(keywords)):
            keywords_news = keywords[i].key_news.count()
            if keywords_news > 3:
                keywords_news_list.append(keywords[i])
        for j in range(len(keywords_news_list)):
            data = []
            keywords_list.append(keywords_news_list[j].keyword)
            for k in range(7):
                time_b = time_a - timedelta(days=7)
                time_b = time_b + timedelta(days=k)
                time_c = time_b - timedelta(days=1)
                time_d = time_b + timedelta(days=1)
                time_b = time_b.strftime("%Y-%m-%d")
                time_c = time_c.strftime("%Y-%m-%d")
                time_d = time_d.strftime("%Y-%m-%d")
                if time_b not in time_list:
                    time_list.append(time_b)
                keywords_news_count = keywords_news_list[j].key_news.\
                    filter(News.datetime.between(time_c, time_d), News.site_id == site_id).count()
                data.append(keywords_news_count)
            if not any(data):
                keywords_list.pop(-1)
            else:
                data_list.append(data)
        source = []
        series = []
        time_list.insert(0, "product")
        source.append(time_list)
        for l in range(len(data_list)):
            data_list[l].insert(0, keywords_list[l])
            source.append(data_list[l])
            series.append({'type': 'bar', 'seriesLayoutBy': 'row'})
        for m in range(len(time_list)-1):
            series.append({'type': 'bar', 'xAxisIndex': 1, 'yAxisIndex': 1})
        site_name = Site.query.filter(Site.id == site_id).first().name
        return {"source": source, "series": series, "site_name": site_name}, 200
