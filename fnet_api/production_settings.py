from .get_env import get_env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': get_env("MYSQL_HOST", "fnet-mysql"),
        'PORT': get_env("MYSQL_PORT", "3306"),
        'NAME': get_env("MYSQL_DATABASE"),
        'USER': get_env("MYSQL_USER"),
        'PASSWORD': get_env("MYSQL_PASSWORD")
    }
}

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATA_DIR = "/data"