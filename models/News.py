from configs.database import db
from models.Secondary import news_keyword
import datetime


class News(db.Model):
    """
    The model of the news
    """

    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(255), nullable=False)

    link = db.Column(db.String(255), nullable=False)

    hot = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(255), nullable=False)

    intro = db.Column(db.Text, nullable=False)

    datetime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now)

    pass1 = db.Column(db.String(255), nullable=True)

    pass2 = db.Column(db.String(255), nullable=True)

    pass3 = db.Column(db.String(255), nullable=True)

    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))

    keywords = db.relationship('Keyword', secondary=news_keyword)
