'''
Use this to populate the codes collection with unique hashes.
'''

import pymongo
from random import choice
from string import ascii_lowercase

mongo_con = pymongo.Connection("localhost", 27017)
mongo_db = mongo_con['app_name']  # add app name
mongo_db.authenticate('admin', 'password')  # add mongodb password


def hash_table():
    table = []
    for x in range(50 * 7 * 1000):
        table.append(''.join(choice(ascii_lowercase) for x in range(6)))
    return list(set(table))


hash_table = hash_table()

for code in hash_table:
    mongo_db.codes.insert({"_id": code})
