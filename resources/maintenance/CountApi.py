from flask_restful import Resource
from models.Counter import Counter
from datetime import datetime
from configs.database import db


class CounterApi(Resource):
    """
    :return counts
    """
    @staticmethod
    def get():
        """
        counts the number of view counts
        :return: number
        """
        counts = Counter.query.count()
        return {"counts": counts}, 200

    @staticmethod
    def post():
        """
        add count record into the counter database
        :return: success or error message
        """
        count_record = Counter(
            create_time=datetime.now()
        )
        db.session.add(count_record)
        db.session.commit()
        return {"message": "success"}, 201
