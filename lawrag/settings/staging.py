from .production import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INSTALLED_APPS += ["silk"]

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]
