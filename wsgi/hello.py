#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import cgi
import bottle
import pymongo
import datetime
from random import choice
from string import ascii_lowercase



bottle.debug(True)

mongo_con = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_HOST'],
                            int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))

mongo_db = mongo_con[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'],
                            os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'])
bottle.TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'],
                                                'wsgi', 'views'))


@bottle.route('/')
def index():
    restaurants = mongo_db.restaurants.find()
    body = "<h1>Welcome to Spokane Restaurant Week</h1>"
    return bottle.template('index', body=body, restaurants=restaurants)


# @bottle.route('/get_code/:name')
# def get_code():
#     collection = mongo_db.restaurants
#     collection.find('name')
#     ''.join(choice(ascii_lowercase) for x in range(6))


def insert_restaurant(restaurant):
    collection = mongo_db.restaurants
    exp = re.compile('\W')  # match anything not alphanumeric
    whitespace = re.compile('\s')
    temp_link = whitespace.sub("-", restaurant)
    permalink = exp.sub('', temp_link).lower()
    data = {
        "name": restaurant,
        "permalink": permalink,
        "codes": []
    }
    collection.insert(data)


# @bottle.route('/insert-restaurants')
# def insert_restaurants():
#     for restaurant in restaurants:
#         insert_restaurant(restaurant)


@bottle.route('/restaurants/')
def list_restaurants():
    restaurants = mongo_db.restaurants.find()
    body = "<p>Pick a restaurant from the left</p>"
    return bottle.template('index', body=body, restaurants=restaurants)


@bottle.get('/restaurants/<permalink>')
def show_restaurant(permalink):
    restaurants = mongo_db.restaurants.find()
    permalink = cgi.escape(permalink)
    restaurant = mongo_db.restaurants.find_one({"permalink": permalink})
    if restaurant:
        body = "<h1>{}</h1>".format(restaurant['name'])

    return bottle.template('index', body=body, restaurants=restaurants)



application = bottle.default_app()
