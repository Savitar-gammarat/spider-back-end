from flask_restful import Resource
from models.Counter import Counter
from datetime import datetime
from configs.database import db, to_dict
from configs.config import cache


class LoginAnalysisApi(Resource):
    """
    :return counts
    """

    @cache.cached(timeout=300)
    def get(self):
        """
        counts the number of view counts group by time
        :return: two list:time list and number list
        """
        x = []
        y = []
        counter = 0
        counts = Counter.query.all()
        for i in range(len(counts)):
            time = counts[i].create_time.strftime("%Y/%m/%d")
            if time not in x:
                x.append(time)
                if counter != 0:
                    y.append(counter)
                counter = 1
            else:
                counter += 1
        y.append(counter)
        return {
            "loginAnalysis": {
                "x": x, "y": y
                }
            }, 200

