#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import bottle
import pymongo
import datetime
from random import choice
from string import ascii_lowercase

restaurants = ["Anthony's at Spokane Falls",
"Bistango Martini Lounge",
"Casper Fry",
"Central Food",
"Churchill's Steakhouse",
"Ciao Mambo",
"Clinkerdagger",
"Hills' Restaurant and Lounge",
"Hugos On The Hill",
"Italia Trattoria",
"Laguna Cafe",
"Luigi's Italian Restaurant",
"MacKenzie River Pizza, Grill & Pub (North)",
"MacKenzie River Pizza, Grill & Pub (South)",
"Maggie's South Hill Grill",
"MAX at mirabeau",
"Mustard Seed",
"O'Doherty's Irish Grille",
"Post Street Ale House",
"Remington's @Ramada Spokane Airport",
"Ripples Riverside Grill",
"Rock City Grill",
"Saranac Public House",
"Scratch Restaurant & Rain Lounge",
"Spencer's For Steaks And Chops",
"Stacks at Steam Plant",
"Steelhead Bar & Grille",
"Thai Bamboo Restaurants",
"The Palm Court Grill",
"The Q",
"The Safari Room Fresh Grill and Bar",
"Windows of the Seasons"]



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


@bottle.route('/insert-restaurants')
def insert_restaurants():
    for restaurant in restaurants:
        insert_restaurant(restaurant)


@bottle.route('/list-restaurants')
def list_restaurants():
    collection = mongo_db.restaurants
    cursor = collection.find('', {"_id": None})
    for r in cursor:
        print '<a href="/{r[permalink]}">r[name]}</a>\n'.format(r)


application = bottle.default_app()
