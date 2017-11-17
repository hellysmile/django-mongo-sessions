from pymongo import MongoClient
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils.module_loading import import_module
except ImportError:
    from django.utils.importlib import import_module


MONGO_CLIENT = getattr(settings, 'MONGO_CLIENT', None)

if MONGO_CLIENT is not None:
    if isinstance(MONGO_CLIENT, str):
        try:
            module_, attr = MONGO_CLIENT.rsplit('.', maxsplit=1)
            MONGO_CLIENT = getattr(import_module(module_), attr)
        except ModuleNotFoundError:
            raise ImproperlyConfigured(
                'Module "{}" specified by "MONGO_CLIENT"'
                ' setting wasn\'t found'.format(module_))
        except AttributeError:
            raise ImproperlyConfigured(
                'Attribute "{}" specified by "MONGO_CLIENT"'
                ' setting wasn\'t found in module "{}"'.format(attr, module_))

    if not isinstance(MONGO_CLIENT, MongoClient):
        raise ImproperlyConfigured(
            'MONGO_CLIENT attribute has unsupported type "{}".'
            ' Should be the instance of the pymongo.MongoClient class.'
            .format(type(MONGO_CLIENT)))
else:
    MONGO_PORT = int(getattr(settings, 'MONGO_PORT', 27017))
    MONGO_HOST = getattr(settings, 'MONGO_HOST', 'localhost')
    MONGO_DB_USER = getattr(settings, 'MONGO_DB_USER', False)
    MONGO_DB_PASSWORD = getattr(settings, 'MONGO_DB_PASSWORD', False)

    MONGO_CLIENT = MongoClient(
        host=MONGO_HOST,
        port=MONGO_PORT,
    )

    if MONGO_DB_USER and MONGO_DB_PASSWORD:
        MONGO_CLIENT.authenticate(MONGO_DB_USER, MONGO_DB_PASSWORD)

MONGO_DB_NAME = getattr(settings, 'MONGO_DB_NAME', 'test')
MONGO_CLIENT = MONGO_CLIENT[MONGO_DB_NAME]

try:
    MONGO_DB_VERSION = MONGO_CLIENT.connection.server_info()['version']
except TypeError:
    # for pymongo >= 3
    MONGO_DB_VERSION = MONGO_CLIENT.client.server_info()['version']

if not float('.'.join(MONGO_DB_VERSION.split('.')[:-1])) >= 2.2:
    raise ImproperlyConfigured(
        '''
        Your mongodb service doesn't support TTL
        http://docs.mongodb.org/manual/tutorial/expire-data/
        '''
    )

MONGO_SESSIONS_COLLECTION = getattr(
    settings, 'MONGO_SESSIONS_COLLECTION', 'mongo_sessions'
)

# think twice before change it
# sessionid cookie will get different expiration time
MONGO_SESSIONS_TTL = getattr(
    settings, 'MONGO_SESSIONS_TTL', settings.SESSION_COOKIE_AGE
)

DB_COLLECTION = MONGO_CLIENT[MONGO_SESSIONS_COLLECTION]

MONGO_SESSIONS_INDEXES = DB_COLLECTION.index_information()

# check existing indexes
if len(MONGO_SESSIONS_INDEXES) <= 1:
    DB_COLLECTION.ensure_index(
        'session_key',
        unique=True
    )

    DB_COLLECTION.ensure_index(
        'creation_date',
        expireAfterSeconds=MONGO_SESSIONS_TTL
    )

    MONGO_SESSIONS_INDEXES = DB_COLLECTION.index_information()

# change creation_date index if, MONGO_SESSIONS_TTL was changed
if int(MONGO_SESSIONS_INDEXES['creation_date_1']['expireAfterSeconds']) \
        != int(MONGO_SESSIONS_TTL):
    DB_COLLECTION.drop_index('creation_date_1')

    DB_COLLECTION.ensure_index(
        'creation_date',
        expireAfterSeconds=MONGO_SESSIONS_TTL
    )

    MONGO_SESSIONS_INDEXES = DB_COLLECTION.index_information()
