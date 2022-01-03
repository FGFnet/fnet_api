from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fnet',
        'USER': 'fnet',
        'PASSWORD': 'fnet',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATA_DIR = f"{BASE_DIR}/data/django"