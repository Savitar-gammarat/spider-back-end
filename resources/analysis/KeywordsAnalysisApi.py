from flask_restful import Resource
from models.Keyword import Keyword
from models.Counter import Counter
from datetime import datetime, timedelta
from configs.database import db, to_dict
from models.Site import Site
from models.News import News
from configs.config import cache
from flask import request
import jieba
from bin.keywords import run


class KeywordsAnalysisApi(Resource):
    @staticmethod
    # @cache.cached(timeout=600)
    def post():
        try:
            site_id = request.get_json()["site_id"]
            start_time = request.get_json()["start_time"]
            end_time = request.get_json()["end_time"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        result = run(site_id, start_time, end_time, 10)
        time_list = []
        source = []
        series = []
        for key in result[0]:
            time_list.append(key)
        time_list.pop(0)
        time_list.insert(0, "product")
        source.append(time_list)
        for item in result:
            source_items = []
            for i in item.keys():
                source_items.append(item[i])
            source.append(source_items)
        for j in range(len(time_list)):
            series.append({'type': 'bar', 'xAxisIndex': 1, 'yAxisIndex': 1})
        for k in range(len(source)-1):
            series.append({'type': 'bar', 'seriesLayoutBy': 'row'})
        site_name = Site.query.filter(Site.id == site_id).first().name
        return {"source": source, "series": series, "site_name": site_name}, 200
        # keywords_news_list = []
        # time_list = []
        # keywords_list = []
        # data_list =[]
        # time_a = datetime.now()
        # time_b = time_a - timedelta(days=7)
        # keywords = Keyword.query.filter(Keyword.datetime > time_b).all()
        # for i in range(len(keywords)):
        #     keywords_news = keywords[i].key_news.count()
        #     if keywords_news > 3:
        #         keywords_news_list.append(keywords[i])
        # for j in range(len(keywords_news_list)):
        #     data = []
        #     keywords_list.append(keywords_news_list[j].keyword)
        #     for k in range(7):
        #         time_b = time_a - timedelta(days=7)
        #         time_b = time_b + timedelta(days=k)
        #         time_c = time_b - timedelta(days=1)
        #         time_d = time_b + timedelta(days=1)
        #         time_b = time_b.strftime("%Y-%m-%d")
        #         time_c = time_c.strftime("%Y-%m-%d")
        #         time_d = time_d.strftime("%Y-%m-%d")
        #         if time_b not in time_list:
        #             time_list.append(time_b)
        #         keywords_news_count = keywords_news_list[j].key_news.\
        #             filter(News.datetime.between(time_c, time_d), News.site_id == site_id).count()
        #         data.append(keywords_news_count)
        #     if not any(data):
        #         keywords_list.pop(-1)
        #     else:
        #         data_list.append(data)
        # source = []
        # series = []
        # time_list.insert(0, "product")
        # source.append(time_list)
        # for l in range(len(data_list)):
        #     data_list[l].insert(0, keywords_list[l])
        #     source.append(data_list[l])
        #     series.append({'type': 'bar', 'seriesLayoutBy': 'row'})
        # for m in range(len(time_list)-1):
        #     series.append({'type': 'bar', 'xAxisIndex': 1, 'yAxisIndex': 1})
        # site_name = Site.query.filter(Site.id == site_id).first().name
        # return {"source": source, "series": series, "site_name": site_name}, 200

    @staticmethod
    def get():
        try:
            args = request.args
            seg = args["keyword"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406
        seg_list = jieba.cut(seg, cut_all=False)
        msg_list = []
        options = []
        for seg in seg_list:
            msg_list.append(seg)
        try:
            keyword_news = Keyword.query.filter(Keyword.keyword.in_(msg_list)).first().key_news.all()
        except AttributeError:
            return {"error": "there is no such keywords!"}, 403
        for key in msg_list:
            keyword_news_list = Keyword.query.filter(Keyword.keyword == key).first()
            if keyword_news_list is None:
                break
            else:
                keyword_news_list = keyword_news_list.key_news.all()
                x = []
                y = []
                length = len(keyword_news_list)
                count = 0
                for i in range(length):
                    news = keyword_news_list[i]
                    news_time = news.datetime.strftime("%Y-%m-%d")
                    if news_time not in x:
                        x.append(news_time)
                        if count != 0:
                            y.append(count)
                        count = 1
                    else:
                        count += 1
                y.append(count)
            options.append({
                'option': {
                    'title': {
                        'text': '全站点关键字<'+key+'>出现频率',
                        'subtext': '新闻数量以网站所展现新闻为基准',
                    },
                    'tooltip': {
                        'trigger': 'axis',
                        'axisPointer': {
                            'type': 'shadow'
                        }
                    },
                    'xAxis': {
                        'type': 'category',
                        'data': x
                    },
                    'yAxis': {
                        'type': 'value'
                    },
                    'series': [{
                        'data': y,
                        'type': 'line',
                        'smooth': 'true'
                    }]
                }
            })
        time = datetime.now().strftime("%Y-%m-%d")
        return {'data': {"options": options, "datetime": time}}, 200
