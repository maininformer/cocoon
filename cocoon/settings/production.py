
from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['cocoon-healthcare.herokuapp.com']

DATABASES={'default':dj_database_url.config(env='CLEARDB_DATABASE_URL')}
