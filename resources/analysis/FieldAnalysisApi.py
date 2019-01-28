from flask_restful import Resource
from models.Counter import Counter
from datetime import datetime
from configs.database import db, to_dict
from models.Field import Field
from models.News import News


class FieldAnalysisApi(Resource):

    @staticmethod
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
            news = fields[i].field_news
            value = []
            for j in range(len(news)):
                if news[j].status == 1 and news[j].datetime > datetime.strptime("2019-1-24", '%Y-%m-%d'):
                    value.append(news[j])
            data_dict = {
                "value": len(value),
                "name": fields_list[i]
            }
            data.append(data_dict)
        return {"fields": fields_list, "data": data}, 200

