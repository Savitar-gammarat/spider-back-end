from configs.database import db
from models.Secondary import news_field
from configs.config import cache


class Field(db.Model):
    """
    the table of field
    """

    __talbename__ = 'field'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    field = db.Column(db.String(60), nullable=False)

    field_news = db.relationship('News', secondary=news_field, backref=db.backref('fields', lazy='dynamic'),
                                 lazy='dynamic')

    @staticmethod
    # @cache.cached(timeout=60, key_prefix='all_fields')
    def all_fields():
        """
        :return: all the fields
        """
        Fields = Field.query.all()
        return Fields

