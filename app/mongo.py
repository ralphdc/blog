#!/usr/bin/env python3

import pymongo
from app import app

MongoConnection = pymongo.MongoClient(host=app.config.get('MONGO_HOST'), port=app.config.get('MONGO_PORT'))

mongodb = MongoConnection[app.config.get('MONGO_DB')]

mongodb.authenticate(app.config.get('MONGO_USER'), app.config.get('MONGO_PWD'))