import pymysql
import datetime


class Dater(object):
    def __init__(self, date):
        self.date = date

    def date_clear(self):
        if type(self.date) is str:
            try:
                return datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S").replace(hour=0, minute=0, second=0)
            except:
                print("date数据格式错误,应为datetiem.datetime，或为字符串且格式为XXXX-XX-XX XX:XX:XX")
        elif type(self.date) is datetime.datetime:
            return self.date.replace(hour=0, minute=0, second=0)
        else:
            print("date数据类型错误,应为datetiem.datetime，或为字符串且格式为XXXX-XX-XX XX:XX:XX")

    def date_plus(self):
        if type(self.date) is str:
            try:
                return datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S").replace(hour=23, minute=59, second=59)
            except:
                print("date数据格式错误,应为datetiem.datetime，或为字符串且格式为XXXX-XX-XX XX:XX:XX")
        elif type(self.date) is datetime.datetime:
            return self.date.replace(hour=23, minute=59, second=59)
        else:
            print("date数据类型错误,应为datetiem.datetime，或为字符串且格式为XXXX-XX-XX XX:XX:XX")


    def day_plus(self, days):
        interval = datetime.timedelta(days=days)
        if type(self.date) is str:
            try:
                return datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S") + interval
            except:
                print("date数据格式错误,应为datetiem.datetime，或为字符串且格式为XXXX-XX-XX XX:XX:XX")
        elif type(self.date) is datetime.datetime:
            return self.date + interval
        else:
            print("date数据类型错误,应为datetiem.datetime，或为字符串且格式为XXXX-XX-XX XX:XX:XX")

    def day_minus(self, day_end):
        if type(self.date) is str and type(day_end) is str:
            try:
                return (datetime.datetime.strptime(day_end, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")).days
            except:
                print("date或date_end数据格式错误,应同为datetiem.datetime，或同为字符串且格式为XXXX-XX-XX XX:XX:XX")
        elif type(self.date) is datetime.datetime and type(day_end) is datetime.datetime:
            return (day_end - self.date).days
        else:
            print("date或date_end数据格式错误,应同为datetiem.datetime，或同为字符串且格式为XXXX-XX-XX XX:XX:XX")


class Query(object):
    conn = pymysql.connect(host="47.101.196.53", port=3306, user='root', passwd='991004', db='news-aggregation',
                           charset='utf8')
    cursor = conn.cursor()

    def query_all(self, site_id, start, end, numb):    #site_id: 站点id   start:时间段开始日期   end:时间段结束日期   numb:所求关键词的个数

        self.cursor.execute("SELECT COUNT(*) as summary,keyword_id,(SELECT keyword.keyword FROM keyword WHERE keyword.id = keyword_id) as haha FROM (SELECT * FROM news_keyword WHERE news_id in (SELECT id FROM news WHERE site_id=%s AND datetime BETWEEN %s AND %s)) AS b GROUP BY keyword_id ORDER BY summary DESC LIMIT %s",(site_id, start, end, numb))
        result = self.cursor.fetchall()
        llll = list()
        for i in result:
            item = dict()
            item['keyword_id'] = i[1]
            item['keyword'] = i[2]
            llll.append(item)
        return llll

    def query_one(self, keyword_id, date, site_id):    #keyword_id:关键词id,   date:某一天的日期，   site_id:站点id
        date_1 = Dater(date).date_clear()
        date_2 = Dater(date).date_plus()
        self.cursor.execute("SELECT COUNT(*) FROM news WHERE id IN (SELECT news_id FROM news_keyword WHERE keyword_id = %s) AND datetime BETWEEN %s AND %s AND site_id = %s",(keyword_id, date_1, date_2, site_id))
        result = self.cursor.fetchone()
        return result[0]


def run(site_id, start_date, end_date, numb):   #总控制函数，site_为站点号，start_date与end_date分别为时间段的开始日期的结束日期，numb为所求的关键词的个数（如前5个，前10个等等）
    keyword_list = Query().query_all(site_id, start_date, end_date, numb)
    result = list()
    for i in keyword_list:
        item = dict()
        item['keyword'] = i['keyword']
        for x in range(Dater(start_date).day_minus(end_date) + 1):
            date = Dater(start_date).day_plus(x)
            item[str(datetime.datetime.strftime(date, "%Y-%m-%d"))] = Query().query_one(i['keyword_id'], date, site_id)
        result.append(item)
    return result


# if __name__ == '__main__':
#     result = run(2, '2019-01-15 01:02:03', '2019-02-20 01:02:03', 10)