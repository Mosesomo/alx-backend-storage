#!/usr/bin/env python3
'''top student'''
import pymongo


def top_students(mongo_collection):
    '''function that returns all students sorted by average score'''

    average_score = mongo_collection.aggregate([
        {
            "$project":
            {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort":
            {
                "averageScore": -1
            }
        }
    ])

    return average_score
