"""
Configuration class to define the properties used with the application.
The config is initialized based on the application environment (Dev, QA, PROD).

"""
import os


def get_secret(name):
    """
    Method to get the value either from the environment variable or
    from the docker secrets

    :param name:
    :return:
    """
    # Get value from environment variable
    sec_from_env = os.getenv(name)

    if sec_from_env is not None:
        return sec_from_env

    # Get value from Docker Secrets (mostly used by development env)
    secret_path = f'/run/secrets/{name}'
    existence = os.path.exists(secret_path)
    sec_from_docker = None
    if existence:
        sec_from_docker = open(secret_path, encoding='utf-16').read().rstrip('\n')
        return sec_from_docker

    # Return error, if value not configured for the environment
    if all([sec_from_docker is None, not existence]):
        return KeyError(f'{name}')


class Config(object):
    """
    Common Config for the all environments
    """
    TWITTER_URL = 'https://api.twitter.com'
    TWITTER_CONSUMER_KEY = get_secret('twitter_consumer_key')
    TWITTER_CONSUMER_SECRET = get_secret('twitter_consumer_secret')
    BEARER_TOKEN = get_secret('TWITTER_BEARER_TOKEN')


class DevelopmentConfig(Config):
    """
    Config for development
    """
    MYSQL_ROOT_HOST = get_secret('mysql_root_host')
    MYSQL_ROOT_PORT = get_secret('mysql_root_port')
    MYSQL_ROOT_USER = get_secret('mysql_root_user')
    MYSQL_ROOT_PWD = get_secret('mysql_root_pwd')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PWD}@{MYSQL_ROOT_HOST}:{MYSQL_ROOT_PORT}/twtappdb?auth_plugin=mysql_native_password'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Config for Production
    """
    MYSQL_ROOT_HOST = get_secret('mysql_root_host')
    MYSQL_ROOT_PORT = get_secret('mysql_root_port')
    MYSQL_ROOT_USER = get_secret('mysql_root_user')
    MYSQL_ROOT_PWD = get_secret('mysql_root_pwd')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PWD}@{MYSQL_ROOT_HOST}:{MYSQL_ROOT_PORT}/twtappdb?auth_plugin=mysql_native_password'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
