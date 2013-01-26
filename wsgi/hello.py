#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import bottle
import pymongo


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

    return "hello %s" % item['name']


application = bottle.default_app()
