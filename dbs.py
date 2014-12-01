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

    def searchurlpattern(self, url, method):
        i = filter(lambda o: o['pattern'].match(url) is not None, self.l)
        log.debug(i)
        if len(i) > 0:
            return i[0]
        else:
            return None

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
                "pattern": re.compile(_converttoregex(url)),
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
        i[0]['pattern'] = re.compile(_converttoregex(url))

        self.__savestate()


def _converttoregex(pattern):
    i = 0
    result = ""
    while i < len(pattern):
        if pattern[i] == "<":
            var, newi = _scanvar(pattern[i:])
            if var is None:
                print("error parsing variable")
            i = newi + i
            result += "\w*"
        else:
            result += pattern[i]
        i = i + 1

    return result


def _scanvar(pattern):
    i = 1
    while len(pattern) > i and pattern[i] != ">":
        i += 1
    if pattern[i] != ">":
        print(i)
        return None, i

    var = pattern[1:i]
    log.debug("var found: {}".format(var))
    return pattern[0:i], i

