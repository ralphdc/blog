#!/usr/bin/env python3

from .import_illegal_items import import_illegal_items

class BgCommand():

    bg_dict = {
        'illegal': import_illegal_items
    }

    @classmethod
    def get_unit(cls, *args, **kwargs):
        action = args[0] or None
        if action in cls.bg_dict:
            return cls.bg_dict.get(action)(**kwargs)
        else:
            raise Exception("[Error] - action error! item not found!")