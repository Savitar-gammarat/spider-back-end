from configs.database import db
from models.Secondary import news_keyword
import datetime


class Keyword(db.Model):
    """
    the model of keywords
    """

    __tablename__ = 'keyword'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    keyword = db.Column(db.String(27), nullable=False)

    datetime = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.datetime.now)

    key_news = db.relationship('News', secondary=news_keyword, backref=db.backref('keywords', lazy='dynamic'),
                               lazy='dynamic')
