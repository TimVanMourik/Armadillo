from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

GA_ID      = os.environ['GA_ID']
BASE_URL   = 'https://armadillo-brain.herokuapp.com'
