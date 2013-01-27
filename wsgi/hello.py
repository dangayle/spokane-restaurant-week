#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import cgi
import bottle
import pymongo
import datetime
import twilio.twiml
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


def insert_restaurant(restaurant):
    '''
    Insert restaurant record into db.
    '''

    collection = mongo_db.restaurants
    exp = re.compile('\W')  # match anything not alphanumeric
    whitespace = re.compile('\s')  # match space
    temp_link = whitespace.sub("-", restaurant)  # replace spaces
    permalink = exp.sub('', temp_link).lower()
    data = {
        "name": restaurant,
        "permalink": permalink,
        "codes": []
    }
    collection.insert(data)


@bottle.get('/')
def index():
    '''
    Create home page.
    TODO: Add more info
    '''

    restaurants = mongo_db.restaurants.find().sort([('permalink', pymongo.ASCENDING)])
    body = "<h1>Welcome to Spokane Restaurant Week</h1>"
    return bottle.template('index', body=body, restaurants=restaurants)


@bottle.get('/restaurants/')
def list_restaurants():
    '''
    List restaurants.
    TODO: Make more useful
    '''

    restaurants = mongo_db.restaurants.find().sort([('permalink', pymongo.ASCENDING)])
    body = "<p>Pick a restaurant from the left</p>"
    return bottle.template('index', body=body, restaurants=restaurants)


@bottle.get('/restaurants/<permalink>')
def show_restaurant(permalink):
    '''
    Display name + button to get code.
    TODO: Could be more useful, show aggregate data
    '''

    permalink = cgi.escape(permalink)
    restaurants = mongo_db.restaurants.find().sort([('permalink', pymongo.ASCENDING)])
    restaurant = mongo_db.restaurants.find_one({"permalink": permalink})
    if restaurant:
        body = '''
        <div class="hero-unit">
        <h1>{name}</h1>
        <hr />
        <p>Number of visits: {count}</p>
        <p><a class="btn btn-primary btn-large" href="/restaurants/{permalink}/getcode">Get Code <i class="icon-plus"></i></a>
        </div>
        '''.format(
            name=restaurant['name'],
            count=len(restaurant['codes']),
            permalink=permalink)

    return bottle.template('index', body=body, restaurants=restaurants)


@bottle.get('/restaurants/<permalink>/getcode')
def get_code(permalink):
    '''
    Grab a unique 7 digit ascii hash from code table, assign to a restaurant.
    '''

    permalink = cgi.escape(permalink)
    restaurants = mongo_db.restaurants.find().sort([('permalink', pymongo.ASCENDING)])
    restaurant = mongo_db.restaurants.find_one({"permalink": permalink})
    code = mongo_db.codes.find_one()
    mongo_db.restaurants.update({"permalink": permalink}, {"$addToSet": {"codes": code['_id']}})
    mongo_db.codes.remove({"_id": code['_id']})

    body = '''
    <div class="hero-unit">
    <h1>{name}</h1>
    <hr />
    <p>Number of visits: {count}</p>
    <p>Use this code: <code class="lead">{code}</code></p>
    <p><a class="btn btn-primary btn-large" href="/restaurants/{permalink}/getcode">Get Code <i class="icon-plus"></i></a></p>
    </div>
    '''.format(
            name=restaurant['name'],
            code=code['_id'],
            count=len(restaurant['codes']),
            permalink=permalink)

    return bottle.template('index', body=body, restaurants=restaurants)


@bottle.route('/sms/', method="post")
def get_sms(code=0):
    '''
    Respond to twilio sms
    '''

    forms = bottle.request.forms  # TODO: Why can't I simply use this dict?
    d = {}
    for x, y in forms.iteritems():
        d[x] = y
    mongo_db.sms.insert(d)

    #: validate code given in sms, do something with that

    in_restaurant = mongo_db.restaurants.find_one({"codes": d['Body'].lower()})
    in_sms = mongo_db.sms.find({"Body": d['Body'].lower()})
    if in_restaurant and (in_sms.count() < 1):
        mongo_db.restaurants.update({"_id": in_restaurant['_id']}, {'$inc': {"visits": 1}})

    # Set counter cookie @twilio
    count = int(bottle.request.cookies.get('counter', '0'))
    count += 1
    bottle.response.set_cookie('counter', str(count))

    if count == 1:
        message = "Your code has been successfully entered. Please give us your full name to continue."
    else:
        message = 'You have responded %d times' % count

    resp = twilio.twiml.Response()
    resp.sms(message)
    return str(resp)

application = bottle.default_app()
