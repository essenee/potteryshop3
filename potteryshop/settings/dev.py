from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Access enviropsent variables
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WAGTAILADMIN_BASE_URL='127.0.0.1:8000'
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

try:
    from .local import *
except ImportError:
    pass
