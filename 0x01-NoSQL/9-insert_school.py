#!/usr/bin/env python3
'''Insert'''
import pymongo


def insert_school(mongo_collection, **kwargs):
    '''
        function that inserts a new document
        in a collection based on kwargs
    '''

    data = mongo_collection.insert_one(kwargs)
    return data.inserted_id
