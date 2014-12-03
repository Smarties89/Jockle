#!/bin/python
# coding: utf-8
# Standard libraries
import logging
import shelve
import re
from uuid import uuid1

# Third party libraries

# My libraries

log = logging.getLogger()



class RouteDatabaseShelve:
    def __init__(self, fn):
        self.fn = fn

        s = shelve.open(fn)
        if not "l" in s:
            self.l = []
        else:
            self.l = s['l']
        s.close()

    def __savestate(self):
        f = shelve.open(self.fn)
        f['l'] = self.l
        f.close()

    def insertroute(self, url, method, type, returndata, returncode):
        self.l.append(
            {
                "url": url,
                "method": method,
                "type": type,
                "returndata": returndata,
                "returncode": returncode,
                "id": str(uuid1())
            })
        self.__savestate()

    def listpaths(self):
        return self.l

    def update(self, id, url, method, type,returndata, returncode):
        i = filter(lambda o: o['id'] == id, self.l)

        i[0]['url'] = url
        i[0]['method'] = method
        i[0]['type'] = type
        i[0]['returndata'] = returndata
        i[0]['returncode'] = returncode

        self.__savestate()
