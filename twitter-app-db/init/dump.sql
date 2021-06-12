SET NAMES utf8mb4; 

CREATE DATABASE IF NOT EXISTS twtappdb CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

USE twtappdb;

CREATE TABLE IF NOT EXISTS tweets (
	tweet_id varchar(100) NOT NULL,
	app_user_id varchar(100),
	app_user_name varchar(100),
	tweet varchar(1000) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci,
	created_at datetime,
	author_id varchar(100),
	PRIMARY KEY (tweet_id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
