# tests stolen from https://github.com/martinrusev/django-redis-sessions
try:
    # For Django versions < 1.9
    from django.utils.importlib import import_module
except ImportError:
    # For Django versions >= 1.9
    from django.utils.module_loading import import_module

from django.conf import settings
import time
from nose.tools import eq_


session_engine = import_module(settings.SESSION_ENGINE).SessionStore()


def test_modify_and_keys():
    eq_(session_engine.modified, False)
    session_engine['test'] = 'test_me'
    eq_(session_engine.modified, True)
    eq_(session_engine['test'], 'test_me')


def test_save_and_delete():
    session_engine['key'] = 'value'
    session_engine.save()
    eq_(session_engine.exists(session_engine.session_key), True)
    session_engine.delete(session_engine.session_key)
    eq_(session_engine.exists(session_engine.session_key), False)


def test_flush():
    session_engine['key'] = 'another_value'
    session_engine.save()
    key = session_engine.session_key
    session_engine.flush()
    eq_(session_engine.exists(key), False)


def test_items():
    session_engine['item1'], session_engine['item2'] = 1, 2
    session_engine.save()
    # Python 3.*
    eq_(sorted(list(session_engine.items())), [('item1', 1), ('item2', 2)])


def test_expiry():
    # Test if the expiry age is set correctly
    eq_(session_engine.get_expiry_age(), settings.SESSION_COOKIE_AGE)
    session_engine['key'] = 'expiring_value'
    session_engine.save()
    key = session_engine.session_key
    eq_(session_engine.exists(key), True)
    time.sleep(11)
    eq_(session_engine.exists(key), False)


def test_save_and_load():
    session_engine.setdefault('item_test', 8)
    session_engine.save()
    session_data = session_engine.load()
    eq_(session_data.get('item_test'), 8)
