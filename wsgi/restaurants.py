import re
import os
import bottle
import pymongo


bottle.debug(True)

mongo_con = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_HOST'],
                            int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))

mongo_db = mongo_con[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'],
                            os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'])
bottle.TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'],
                                                'wsgi', 'views'))


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
