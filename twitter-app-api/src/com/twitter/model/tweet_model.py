from src.com.twitter.dao.database import db


class Tweets(db.Model):
    tweet_id = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    orig_tweet_id = db.Column(db.String(100), unique=False, nullable=True)
    tweet = db.Column(db.String(1000), unique=False, nullable=True)
    time = db.Column(db.Date(), unique=False, nullable=True)

    def __repr__(self):
        return "<Tweet: {}>".format(self.tweet_id)
