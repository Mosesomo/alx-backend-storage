#!/usr/bin/env python3
'''List all'''
import pymongo


def list_all(mongo_collection):
    '''
        Function that list all the collection
    '''

    if mongo_collection is None:
        return []
    documents = mongo_collection.find()
    return [document for document in documents]
