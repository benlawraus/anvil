from unittest.mock import Mock

from .anvilJs import *


class ExternalError(Exception):
    pass


class window(Mock):
    def Function(*args, **kwargs):
        return Mock()

    class Array(list):
        pass

    class WeakMap(dict):
        def __missing__(self, key):
            return None

    def get(self, *args, **kwargs):
        return Mock()

    def clearTimeout(self):
        pass

    def clearInterval(self):
        pass

    class Promise:
        def __init__(self, *args, **kwargs):
            # this is for the case in anvil_extras.storage.py:
            # _window.Promise(lambda res, rej: self._store.removeItem(key))
            if callable(args[0]):
                args[0](1, 2)  # res, rej
            return

        def all(self, *args, **kwargs):
            return Mock()

    document = Mock()
    document.body = Mock()

    jQuery = Mock()
    jQuery.appendTo = Mock()

    def addEventListener(*args, **kwargs):
        return Mock()

    def removeEventListener(*args, **kwargs):
        return Mock()

    class Object:
        @classmethod
        def keys(cls, obj):
            return [_ for _ in obj.keys()]
