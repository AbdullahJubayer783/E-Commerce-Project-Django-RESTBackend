from .base import *

ALLOWED_HOSTS = ["*"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("NAME"),
        'USER': env("USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("HOST"),
        'PORT': env("PORT"),
    }
}