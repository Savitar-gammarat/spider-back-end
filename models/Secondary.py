from configs.database import db


news_keyword = db.Table(
    "news_keyword",
    db.Column("news_id", db.Integer, db.ForeignKey("news.id"), primary_key=True),
    db.Column("keyword_id", db.Integer, db.ForeignKey("keyword.id"), primary_key=True)
)

news_field = db.Table(
    "news_field",
    db.Column("news_id", db.Integer, db.ForeignKey("news.id"), primary_key=True),
    db.Column("field_id", db.Integer, db.ForeignKey("field.id"), primary_key=True)
)