from flask_restful import Resource
from models.Counter import Counter
from datetime import datetime, timedelta
from configs.database import db, to_dict
from configs.config import cache


class LoginAnalysisApi(Resource):
    """
    :return counts
    """

    @staticmethod
    def get():
        """
        counts the number of view counts group by time
        :return: two list:time list and number list
        """
        x = []
        y = []
        counter = 0
        counts = Counter.query.all()
        for i in range(len(counts)):
            c_time = counts[i].create_time
            time = c_time.strftime("%Y/%m/%d")
            if time not in x:
                x.append(time)
                if counter != 0:
                    y.append(counter)
                if len(x) >= 2:
                    time_a = datetime.strptime(x[-2], '%Y/%m/%d')
                    time_b = datetime.strptime(x[-1], '%Y/%m/%d')
                    interval = (time_b - time_a).days
                    if interval > 1:
                        for j in range(interval-1):
                            time_c = time_a + timedelta(days=(j+1))
                            x.insert(-1,  time_c.strftime('%Y/%m/%d'))
                            y.append(0)
                counter = 1
            else:
                counter += 1
        y.append(counter)
        # for j in range(len(x)-1):
        #     time_a = datetime.strptime(x[j], '%Y/%m/%d')
        #     time_b = datetime.strptime(x[j+1], '%Y/%m/%d')
        #     interval = (time_b - time_a).days
        #     if interval > 1:
        #         time_c = timedelta(days=1) + time_a
        #         x.insert((j+1), time_c.strftime('%Y/%m/%d'))
        return {
            "loginAnalysis": {
                "x": x, "y": y
                }
            }, 200

