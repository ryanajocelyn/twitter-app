import os


def get_secret(name):
    sec_from_env = os.getenv(name)

    if sec_from_env is not None:
        return sec_from_env

    secret_path = f'/run/secrets/{name}'
    existence = os.path.exists(secret_path)
    sec_from_docker = None
    if existence:
        sec_from_docker = open(secret_path, encoding='utf-16').read().rstrip('\n')
        return sec_from_docker

    if all([sec_from_docker is None, not existence]):
        return KeyError(f'{name}')


class Config(object):
    TWITTER_URL = 'https://api.twitter.com'
    TWITTER_CONSUMER_KEY = get_secret('twitter_consumer_key')
    TWITTER_CONSUMER_SECRET = get_secret('twitter_consumer_secret')


class DevelopmentConfig(Config):
    MYSQL_ROOT_PWD = get_secret('mysql_root_pwd')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{MYSQL_ROOT_PWD}@db/twtappdb?auth_plugin=mysql_native_password'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    BEARER_TOKEN = get_secret('TWITTER_BEARER_TOKEN')


class ProductionConfig(Config):
    DATABASE_URL = None
