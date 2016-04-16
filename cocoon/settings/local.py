
from .base import *
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {'default': dj_database_url.config()}



