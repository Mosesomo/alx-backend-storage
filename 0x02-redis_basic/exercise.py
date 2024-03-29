#!/usr/bin/env python3
'''Writing strings to Redis'''
import redis
import uuid
from typing import Union, Optional


class Cache:
    '''A simple cache class for
        writing data to a Redis server.
    '''

    def __init__(self):
        '''Instance of redis client'''

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            store method that takes a data argument and returns
            a string. The method should generate a random key
            (e.g. using uuid), store the input data
            in Redis using the random key and return the key.
        '''

        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
    
    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        '''
            method that take a key string argument and an optional Callable
            argument named fn. This callable will be used to convert the
            data back to the desired format.
        '''

        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''parametrize Cache.get with the correct conversion function.'''

        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        '''parametrize Cache.get with the correct conversion function.'''

        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0

        return data

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
    
    
