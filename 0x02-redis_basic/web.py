#!/usr/bin/env python3
'''Implementing an expiring web cache and tarcker'''
import redis
import requests
from functools import wraps


redi = redis.Redis()


def accessed_how_many_times(method):
    '''Decorator counting how many times a url is accessed'''

    @wraps(method)
    def wrapper(url):
        key = "count:" + url
        data = redi.get(key)
        if data:
            return data.decode("utf-8")

        count_keys = "count:" + url
        html = method(url)

        redi.incr(count_keys)
        redi.set(key, html)
        redi.expire(key, 10)
        return html
    return wrapper


@accessed_how_many_times
def get_page(url: str) -> str:
    '''Uses requests module to obtain the html content
        of a particular url and returns it
    '''

    response = requests.get(url)
    return response.text
