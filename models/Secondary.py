from configs.database import db


news_keyword = db.Table(
    "news_keyword",
    db.Column("news_id", db.Integer, db.ForeignKey("news.id"), primary_key=True),
    db.Column("keyword_id", db.Integer, db.ForeignKey("keyword.id"), primary_key=True)
)