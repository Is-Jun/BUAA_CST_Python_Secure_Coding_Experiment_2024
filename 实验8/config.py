import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    CAPTCHA_ENABLE = True
    CAPTCHA_NUMERIC_DIGITS = 5
    CAPTCHA_SESSION_KEY = 'captcha_image'


