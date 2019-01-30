from flask_restful import Resource
from models.Counter import Counter
from datetime import datetime
from configs.database import db, to_dict
from models.Site import Site
from models.News import News
from configs.config import cache


class SiteAnalysisApi(Resource):
    @cache.cached(timeout=600)
    def get(self):
        """
        counts the number of news group by site
        :return: two list:field list and data list
        """
        sites_list = []
        data = []
        sites = Site.query.all()
        for i in range(len(sites)):
            name = sites[i].name
            sites_list.append(name)
            news = News.query.filter(News.site_id == (i+1)).all()
            value = len(news)
            data_dict = {
                "value": value,
                "name": name
            }
            data.append(data_dict)
        return {"SiteAnalysis": {"sites": sites_list, "data": data}}, 200

