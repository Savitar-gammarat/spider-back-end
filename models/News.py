from configs.database import db
from models.Secondary import news_keyword, news_field
import datetime


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
