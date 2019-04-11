#!/usr/bin/env python3

import os
from .Develop import Develop
from .Product import Product

def Config():

    cfg_env = os.getenv('RUN_MOD', 'dev')

    if cfg_env == 'dev':
        return Develop()
    elif cfg_env == 'prd':
        return Product()
    else:
        return None 