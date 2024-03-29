#!/usr/bin/env python3
'''Writing strings to Redis'''
import redis
import uuid
from typing import Union


class Cache:
    '''A simple cache class for
        writing data to a Redis server.
    '''

    def __init__(self) -> None:
        '''Instance of redis client'''

        self.__redis = redis.Redis(host='localhost', port=6379, db=0)
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            store method that takes a data argument and returns
            a string. The method should generate a random key
            (e.g. using uuid), store the input data
            in Redis using the random key and return the key.
        '''

        key = str(uuid.uuid4())
        self.__redis.set(key, data)

        return key
