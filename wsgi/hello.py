#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import bottle
import pymongo
import datetime
from random import choice
from string import ascii_lowercase
from restaurants import restaurants


bottle.debug(True)

mongo_con = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_HOST'],
                            int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))

mongo_db = mongo_con[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'],
                            os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'])


@bottle.route('/')
def index():
    collection = mongo_db.test
    item = collection.find_one()
    return "hello %s, you doob" % item['name']


# @bottle.route('/get_code/:name')
# def get_code():
#     collection = mongo_db.restaurants
#     collection.find('name')
#     ''.join(choice(ascii_lowercase) for x in range(6))


@bottle.route('/insert_restaurants')
def insert_restaurants():
    collection = mongo_db.restaurants
    for restaurant in restaurants:
        data = {
            "name": restaurant,
            "codes": []
            }
        collection.insert(data)

application = bottle.default_app()
