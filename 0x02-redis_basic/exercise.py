#!/usr/bin/env python3
'''Writing strings to Redis'''
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''decorator that takes a single method Callable
        argument and returns a Callable.
    '''

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''function that increments the count for
            that key every time the method is called
        '''

        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''store the history of inputs and outpurs'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wraps the decorated function'''

        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    '''display the history of calls of a particular function.'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    '''A simple cache class for
        writing data to a Redis server.
    '''

    def __init__(self):
        '''Instance of redis client'''

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
