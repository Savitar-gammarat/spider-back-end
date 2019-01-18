from configs.database import db
from models.Secondary import news_field


class Field(db.Model):
    """
    the table of field
    """

    __talbename__ = 'field'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    field = db.Column(db.String(60), nullable=False)

    field_news = db.relationship('News', secondary=news_field)
