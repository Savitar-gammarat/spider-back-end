from flask_restful import Resource
from models.Counter import Counter
from datetime import datetime, timedelta
from configs.database import db, to_dict
from models.Field import Field
from models.News import News
from models.Site import Site
from configs.config import cache
from flask import request


class FieldAnalysisApi(Resource):
    @staticmethod
    @cache.cached(timeout=600)
    def get():
        """
        counts the number of news group by field
        :return: two list:field list and data list
        """
        fields = Field.query.all()
        fields_list = []
        data = []
        for i in range(len(fields)):
            fields_list.append(fields[i].field)
            news = fields[i].field_news.all()
            value = []
            for j in range(len(news)):
                if news[j].status == 1 and news[j].datetime > datetime.strptime("2019-1-24", '%Y-%m-%d'):
                    value.append(news[j])
            data_dict = {
                "value": len(value),
                "name": fields_list[i]
            }
            data.append(data_dict)
        return {"fieldAnalysis": {"fields": fields_list, "data": data}}, 200

    @staticmethod
    def post():
        """
        counts the number of news group by field and time according to the site parma
        :return: {time_data:[], sum:{n:: sum_data:[]}, field_list:[]}
        """

        try:
            site_id = request.get_json()["site_id"]
        except KeyError:
            return {"error": "lack necessary argument!"}, 406

        Field_list = []
        time_list = []
        data_list = []
        source = []
        series = []
        Fields = Field.all_fields()
        time_a = datetime.now()
        for i in range(len(Fields)):
            data = []
            Field_list.append(Fields[i].field)
            for j in range(8):
                time_b = time_a - timedelta(days=8)
                time_b = time_b + timedelta(days=j)
                time_c = time_b - timedelta(days=1)
                time_d = time_b + timedelta(days=1)
                time_b = time_b.strftime("%Y-%m-%d")
                time_c = time_c.strftime("%Y-%m-%d")
                time_d = time_d.strftime("%Y-%m-%d")
                if time_b not in time_list:
                    time_list.append(time_b)
                field_news_counts = Fields[i].field_news.filter(News.datetime.between(time_c, time_d),
                                                                News.site_id == site_id).count()
                data.append(field_news_counts)
            data_list.append(data)
        time_list.insert(0, "product")
        source.append(time_list)
        for k in range(len(data_list)):
            data_list[k].insert(0, Field_list[k])
            source.append(data_list[k])
            series.append({"type": 'line', "smooth": "true", "seriesLayoutBy": 'row'})
        series.append({
                "type": 'pie',
                "id": 'pie',
                "radius": '35%',
                "center": ['50%', '25%'],
                "label": {
                    "formatter": '{b}: {@[' + "1" + ']} ({d}%)'
                },
                "encode": {
                    "itemName": 'product',
                    "value": time_list[1],
                    "tooltip": time_list[1]
                }
            })
        site_name = Site.query.filter(Site.id == site_id).first().name
        return {"source": source, "series": series, "site_name": site_name}, 200

