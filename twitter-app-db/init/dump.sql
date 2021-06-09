CREATE DATABASE IF NOT EXISTS twtappdb;

USE twtappdb;

CREATE TABLE IF NOT EXISTS tweets (
	tweet_id varchar(100) NOT NULL,
	orig_tweet_id varchar(100),
	tweet varchar(1000),
	time datetime,
	PRIMARY KEY (tweet_id)
);
