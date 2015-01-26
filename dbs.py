#!/bin/python
# coding: utf-8
# Standard libraries
import logging
import shelve
from uuid import uuid1
from json import loads, dumps
from os.path import isfile


# Third party libraries

# My libraries


log = logging.getLogger("jockle")


class RouteDatabaseShelve:
    def __init__(self, fn):
        self.fn = fn

        s = shelve.open(fn)
        if not "l" in s:
            self.l = []
            self._proxy = {"url": ""}
        else:
            self.l = s['l']
            self._proxy = s['proxy']
        s.close()

    def __savestate(self):
        f = shelve.open(self.fn)
        f['l'] = self.l
        f['proxy'] = self._proxy
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

    def update(self, id, url, method, type, returndata, returncode):
        i = filter(lambda o: o['id'] == id, self.l)

        i[0]['url'] = url
        i[0]['method'] = method
        i[0]['type'] = type
        i[0]['returndata'] = returndata
        i[0]['returncode'] = returncode

        self.__savestate()

    def proxyurl(self):
        return self._proxy['url']

    def setproxyurl(self, url):
        self._proxy['url'] = url
        self.__savestate()

    def delete(self, url):
        self.l = filter(lambda o: o['url'] != url, self.l)
        self.__savestate()


class RouteDatabaseJSON:
    def __init__(self, fn):
        self.fn = fn

        if not isfile(fn):
            with open(fn, "w") as f:
                f.write(dumps(
                    {
                        "proxyurl": "",
                        "api": []
                    }))
        self.__loadstate()

    def __loadstate(self):
        with open(self.fn, "r") as f:
            s = loads(f.read())
            self._api = s['api']
            self._proxy = s['proxyurl']

    def __savestate(self):
        with open(self.fn, "w") as f:
            text = dumps(
                {
                    "api": self._api,
                    "proxyurl": self._proxy
                },
                sort_keys=True,
                indent=4)
            f.write(text)

    def insertroute(self, url, method, type, returndata, returncode, inputtype, inputvars):
        log.info("""Inserting route:
\turl: {}
\tmethod: {}
\ttype: {}
\treturndata: {}
\treturncode: {}
\tinputtype: {}
\tinputvars: {}
""".format(url, method, type, returndata, returncode, inputtype, inputvars))
        self._api.append(
            {
                "url": url,
                "method": method,
                "type": type,
                "returndata": returndata,
                "returncode": returncode,
                "id": str(uuid1()),
                "inputtype": inputtype,
                "inputvars": inputvars
            })
        self.__savestate()

    def listpaths(self):
        return self._api

    def update(self, id, url, method, type, returndata, returncode, inputtype, inputvars):
        i = filter(lambda o: o['id'] == id, self._api)

        i[0]['url'] = url
        i[0]['method'] = method
        i[0]['type'] = type
        i[0]['returndata'] = returndata
        i[0]['returncode'] = returncode
        i[0]['inputtype'] = inputtype
        i[0]['inputvars'] = inputvars

        self.__savestate()

    def proxyurl(self):
        return self._proxy

    def setproxyurl(self, url):
        self._proxy = url
        self.__savestate()

    def delete(self, url):
        self._api = filter(lambda o: o['url'] != url, self._api)
        self.__savestate()
