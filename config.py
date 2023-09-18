from dotenv import dotenv_values

# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
config = dotenv_values(".env")


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = config['SECRET_KEY']

    SQLALCHEMY_DATABASE_URI = f"postgresql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = config['MAIL_SERVER']
    MAIL_PORT = config['MAIL_PORT']
    MAIL_USE_SSL = config["MAIL_USE_SSL"]
    MAIL_USERNAME = config["MAIL_USERNAME"]
    MAIL_PASSWORD = config['MAIL_PASSWORD']


class TestingConfig(Config):
    TESTING = True
