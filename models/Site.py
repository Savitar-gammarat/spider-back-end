from configs.database import db


class Site(db.Model):
    """
    the table of sites
    """

    __talbename__ = 'site'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    name = db.Column(db.String(25), nullable=False)

    pageviews = db.Column(db.Integer, nullable=True)

    color = db.Column(db.String(255), nullable=True)

    logo = db.Column(db.String(255), nullable=True)

    font = db.Column(db.String(255), nullable=True)

    site_news = db.relationship('News', backref='site')
