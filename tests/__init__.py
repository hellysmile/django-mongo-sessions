from django.conf import settings


settings.configure(
    SESSION_ENGINE='mongo_sessions.session',
    SESSION_COOKIE_AGE=10,
    MONGO_DB_USER='hell',
    MONGO_DB_PASSWORD='hell'
)
