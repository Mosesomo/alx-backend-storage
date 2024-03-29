#!/usr/bin/env python3
'''Filter'''
import pymongo


def schools_by_topic(mongo_collection, topic):
    '''
         function that returns the list of
         school having a specific topic
    '''

    filtered = mongo_collection.find({"topics": {"$in": [topic]}})
    return filtered
