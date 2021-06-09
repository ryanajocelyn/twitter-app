from src.com.twitter.dao.database import db
from sqlalchemy_serializer import SerializerMixin


class Tweets(db.Model, SerializerMixin):
    tweet_id = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    orig_tweet_id = db.Column(db.String(100), unique=False, nullable=True)
    author_id = db.Column(db.String(100), unique=False, nullable=True)
    tweet = db.Column(db.String(1000), unique=False, nullable=True)
    time = db.Column(db.Date(), unique=False, nullable=True)

    def __repr__(self):
        return "<Tweet: {}>".format(self.tweet_id)

    def serialize(self):
        return Serializer.serialize(self)
