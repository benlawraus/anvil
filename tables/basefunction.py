from typing import Optional, Dict, List
import pydal.helpers.classes

from tests import pydal_def as mydal
from anvil.tables.query import *


class order_by:
    def __init__(self, *args, **kwargs):
        self.order = '|'.join(args)
        self.kwargs = kwargs


class BaseFunction:
    """Saving rows and getting rows to/from the database"""

    def __init__(self, table_name: str, table_dict: Dict[str, str]):
        self.query: List = []  # list of pydal.objects.Query
        self.table_name: str = table_name
        self.table_dict: Dict[str.str] = table_dict

    def add_row(self, **kwargs) -> pydal.helpers.classes.Reference:
        if self.table_name not in mydal.db.tables:
            raise AttributeError("Table not in database.")
        try:
            reference = mydal.db[self.table_name].insert(**kwargs)
        except TypeError:
            msg = f"\n{self.table_name}:\n fields:\n {kwargs}"
            raise TypeError(msg)
        mydal.db.commit()
        return reference

    def get_by_id(self, uid) -> Optional[pydal.objects.Row]:
        return mydal.db[self.table_name](uid)

    def _pick_apart(self, key, val, _q):
        if len(val.args) > 0:
            for arg in val.args:
                # there must be a key
                _q.append(self.add_to_query(key, arg))
        for _key in val.kwargs:
            # there must be no key
            _q.append(self.add_to_query(_key, val.kwargs[_key]))
        return

    def add_to_query(self, key, val):
        if isinstance(val, all_of):
            _q = []
            self._pick_apart(key, val, _q)
            _query = _q[0]
            if len(_q) > 1:
                for ix in range(1, len(_q)):
                    _query &= (_q[ix])
            return _query
        elif isinstance(val, any_of):
            _q = []
            self._pick_apart(key, val, _q)
            _query = _q[0]
            if len(_q) > 1:
                for ix in range(1, len(_q)):
                    _query |= (_q[ix])
            return _query
        elif isinstance(val, full_text_match):
            return mydal.db[self.table_name][key].contains(val.arg)
        elif isinstance(val, ilike):
            return mydal.db[self.table_name][key].ilike(val.arg)
        elif isinstance(val, like):
            return mydal.db[self.table_name][key].like(val.arg)
        elif isinstance(val, not_):
            return mydal.db[self.table_name][key] != val.arg
        elif isinstance(val, less_than):
            return mydal.db[self.table_name][key] < val.arg
        elif isinstance(val, greater_than):
            return mydal.db[self.table_name][key] > val.arg
        elif isinstance(val, greater_than_or_equal_to):
            return mydal.db[self.table_name][key] >= val.arg
        elif isinstance(val, less_than_or_equal_to):
            return mydal.db[self.table_name][key] <= val.arg
        elif isinstance(val, between):
            if val.kwargs['min_inclusive']:
                _query = mydal.db[self.table_name][key] >= val.arg[0]
            else:
                _query = mydal.db[self.table_name][key] > val.arg[0]
            if val.kwargs['max_inclusive']:
                _query &= mydal.db[self.table_name][key] <= val.arg[1]
            else:
                _query &= mydal.db[self.table_name][key] < val.arg[1]
            return _query
        elif key is not None:
            return mydal.db[self.table_name][key] == val
        else:
            return val

    def _orderby(self, arg):
        ord_for = arg.order.split('|')
        _o = mydal.db[self.table_name][ord_for[0]]
        if len(ord_for) > 1:
            for f in ord_for[1:]:
                _o |= mydal.db[self.table_name][f]
        if 'ascending' in arg.kwargs:
            if not arg.kwargs['ascending']:
                _o = ~_o
        return _o

    def search(self, *args, **kwargs):
        _orderby = {}
        _fetch_only = None
        self.query = None
        if len(args) > 0:
            for arg in args:
                if isinstance(arg, order_by):
                    _orderby = {'orderby': self._orderby(arg)}
                elif isinstance(arg, fetch_only):
                    _fetch_only = arg.args
                else:
                    self.query = self.add_to_query(None, arg)
        #
        for key in kwargs:
            if self.query:
                self.query &= (self.add_to_query(key, kwargs[key]))
            else:
                self.query = self.add_to_query(key, kwargs[key])
        if self.query is None and len(_orderby) == 0:
            self.query = mydal.db[self.table_name]['id'] != None
        if _fetch_only:
            return mydal.db(self.query).select(*_fetch_only, **_orderby)
        return mydal.db(self.query).select(**_orderby)

    def get(self, **kwargs) -> Optional[pydal.objects.Row]:
        return mydal.db[self.table_name](**kwargs)

    def list_columns(self) -> List[Dict[str, str]]:
        field_list = []
        for field in self.table_dict:
            if field == 'id':
                continue
            field_list.append({'name': field, 'type': self.table_dict[field]})
        return field_list

    def delete_all_rows(self):
        mydal.db[self.table_name].truncate()
        mydal.db.commit()
        return
