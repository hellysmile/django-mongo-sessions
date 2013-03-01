from django.conf import settings


settings.configure(
    SESSION_ENGINE='mongo_sessions.session',
    SESSION_COOKIE_AGE=10,
)
