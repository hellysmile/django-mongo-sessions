django-mongo-sessions
=====================
:Info: mongodb as Django sessions backend

.. image:: https://api.travis-ci.org/hellysmile/django-mongo-sessions.png
        :target: https://travis-ci.org/hellysmile/django-mongo-sessions

features
********

* fast NoSQL Django sessions backend
* automatic invalidation by `TTL <http://docs.mongodb.org/manual/tutorial/expire-data/>`_

------------
installation
------------

run ``pip install django-mongo-sessions``

set ``mongo_sessions.session`` as session engine::

    SESSION_ENGINE = 'mongo_sessions.session'

--------
settings
--------

there is two ways to setup mongodb connection at ``settings.py``


first, if already have mongo connection, like::

    import pymongo
    from pymongo import MongoClient
    connection = MongoClient()
    MONGO_CLIENT = connection.your_database
    MONGO_SESSIONS_COLLECTION = 'mongo_sessions' # default option

second, if you need to connect to mongodb, like::

    MONGO_PORT = 27017
    MONGO_HOST = 'localhost'
    MONGO_DB_NAME = 'test'
    MONGO_DB_USER = False
    MONGO_DB_PASSWORD = False
    MONGO_SESSIONS_COLLECTION = 'mongo_sessions'

    # all this settings are defaults, you can skip any

tests::

    pip install tox
    tox
