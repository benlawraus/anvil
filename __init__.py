from collections import UserDict

import pydal.helpers.classes
import pydal.objects

from .anvil_ui import *
from .component import *


class RowDict(UserDict):
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            if isinstance(args[0], pydal.helpers.classes.Reference):
                args_ix = self.loop_attr(args[0]._table._fields, args)
                super().__init__(args_ix)
                return
            elif isinstance(args[0], pydal.objects.Row):
                args_ix = self.loop_attr(args[0].__dict__.keys(), args)
                super().__init__(args_ix)
                return
        super().__init__(*args, **kwargs)
        return

    @staticmethod
    def loop_attr(attr_list, args):
        args_ix = []
        for attr in attr_list:
            if attr in ('id', 'update_record', 'delete_record'):
                continue
            val = args[0][attr]
            args_ix.append((attr, val))
        return args_ix


def dict(*args, **kwargs):
    return RowDict(*args, **kwargs).data


app = Mock()
