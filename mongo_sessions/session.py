from datetime import timedelta
try:
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text as force_unicode
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.utils import timezone
from mongo_sessions import settings


class SessionStore(SessionBase):
    '''
    mongodb as Django sessions backend
    '''
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

        self.db_collection = settings.DB_COLLECTION

    def get_expiry_age(self):
        return settings.MONGO_SESSIONS_TTL

    def get_expiration_date(self):
        return timezone.now() - timedelta(
            seconds=self.get_expiry_age()
        )

    def load(self):
        mongo_session = self.db_collection.find_one({
            'session_key': self._get_or_create_session_key(),
            'creation_date': {
                '$gt': self.get_expiration_date()
            }
        })

        if not mongo_session is None:
            return self.decode(force_unicode(mongo_session['session_data']))
        else:
            self._session_key = None
            return {}

    def exists(self, session_key):
        session = self.db_collection.find_one({
            'session_key': session_key,
        })

        if session is None:
            return False
        else:
            # mongodb ttl invalidation runs only once per minute, delete manually
            if session['creation_date'] <= self.get_expiration_date():
                self.delete(session_key)
                return self.exists(session_key)
            return True

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            # ensure that session key is unique
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        if must_create and self.exists(self.session_key):
            raise CreateError

        session = {
            'session_key': self.session_key,
            'session_data': self.encode(
                self._get_session(no_load=must_create)
            ),
            'creation_date': timezone.now()
        }

        self.db_collection.update(
            {'session_key': self.session_key},
            {'$set': session},
            upsert=True
        )

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self.session_key
        self.db_collection.remove({'session_key': session_key})

    def set_expiry(self, value):
        raise NotImplementedError
