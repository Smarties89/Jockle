#!/bin/python
# coding: utf-8
# Standard libraries
import logging
import json
import datetime
import os

from flask import request


log = logging.getLogger("hest.util")

def randomstring(n=32):
    """ randomstring() -> x where len(x) = n.
    """
    return os.urandom(n).encode("base64")[0:n]


def debug():
    """ debug() -> False if the machine is a production-server.

    Implemented by principle of "better safe than sorry".
    All machines are assumed to be production servers
    unless a file named /notproducserver exists.
    """
    return os.path.isfile("/notprodserver")


class CustomEncoder(json.JSONEncoder):
    """A C{json.JSONEncoder} subclass to encode documents that have fields of
     type C{bson.objectid.ObjectId}, C{datetime.datetime}
    """
    def default(self, obj):
        from bson import ObjectId
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

encode = CustomEncoder().encode


def remote_addr():
    # TODO: clean this up. It works but is hard to understand.
    # Tries to fetch Cf-Connecting-Ip first(if request are through cloudflare service).
    # else it tries to get X-Forwarded-For(if request is only through external ip.
    # else it returns localhost.
    return request.headers.get("Cf-Connecting-Ip",
           request.headers.get("X-Forwarded-For", "localhost"))
