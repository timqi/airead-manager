__author__ = 'airead'


class Default(object):
    APP_NAME = 'flask-angular-seed'
    DEBUG = False
    SECRET_KEY = '\x1e\xfa\xbe1\xf2\xc49\xd6\xb4c\xf1\xb4\t\x9cb\xcf.Og{\x1e\n@\xf7'
    LOG_LEVEL = 'WARNING'
    LOG_DIR = 'logs/'

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class Dev(Default):
    DEBUG = True
    LOG_LEVEL = 'INFO'
    SEND_FILE_MAX_AGE_DEFAULT = 0