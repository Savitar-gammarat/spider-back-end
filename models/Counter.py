from configs.database import db


class Counter(db.Model):
    """
    the table of counter
    """

    __talbename__ = 'counter'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    create_time = db.Column(db.DateTime, nullable=False)
