import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shalom'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pavel:DesMoines88@paveldbmp.csu5cpfwxtxi.us-east-2.rds.amazonaws.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False