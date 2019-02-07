from configs.database import db
from models.Keyword import Keyword
from models.Secondary import news_keyword
import datetime
from configs.config import cache


class News(db.Model):
    """
    The model of the news
    """

    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(255), nullable=False)

    link = db.Column(db.String(255), nullable=False)

    hot = db.Column(db.Float, nullable=False, default=0)

    datetime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now)

    click = db.Column(db.Integer, nullable=True, default=0)

    status = db.Column(db.Integer, nullable=True, default=0)

    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)

    keywords = db.relationship('Keyword', secondary=news_keyword)

    # fields = db.relationship('Field', secondary=news_field)

    @staticmethod
    @cache.cached(timeout=3600, key_prefix='all_news')
    def all_news():
        """
        :return: all news
        """
        all_news = News.query.all()
        return all_news

    @staticmethod
    @cache.cached(timeout=3600, key_prefix='latest_news')
    def latest_news():
        """
        :return: latest 10000 news
        """
        latest_news = News.query.order_by(News.id.desc(), News.datetime.desc()).limit(10000).all()
        return latest_news
