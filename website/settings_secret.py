''' Contains all the secret settings '''
import os

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError:
    DATABASE_URL = 'localhost'

try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    SECRET_KEY = 'uf1og^)2nc6bgr@-qgxr@^4#)b1l3qty)_t84x8%^pt-$(v&)$'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pick',
        'USER': 'pickadmin',
        'PASSWORD': 'p1ckd3m0',
        'HOST': DATABASE_URL,
        'PORT': '',
    }
}
