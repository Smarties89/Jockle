#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from uuid import uuid1
import re
import shelve


from jinja2 import Environment, FileSystemLoader
from cgi import parse_header, parse_multipart
from urlparse import parse_qs


log = logging.getLogger()
dbpath = argv[1]
port = int(argv[2])

env = Environment(loader=FileSystemLoader('templates'))


def render_template(templatefile, **kwargs):
    template = env.get_template(templatefile)
    return template.render(**kwargs)


def debug():
    # TODO: implementer
    return True


if debug():
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
else:
    logging.basicConfig()
    log.setLevel(logging.INFO)


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

    def insertroute(self, url, method, type, data):
        self.l.append(
            {
                "url": url,
                "method": method,
                "type": type,
                "data": data,
                "pattern": re.compile(_converttoregex(url)),
                "id": str(uuid1())
            })
        self.__savestate()

    def listpaths(self):
        return self.l

    def update(self, id, url, method, type, data):
        i = filter(lambda o: o['id'] == id, self.l)

        i[0]['url'] = url
        i[0]['method'] = method
        i[0]['type'] = type
        i[0]['data'] = data
        i[0]['pattern'] = re.compile(_converttoregex(url))

        self.__savestate()


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


db = RouteDatabaseShelve(dbpath)
#db.insertroute("/cards/[\w]*/categories", "POST", "json", '{"status": "hi"}')


class MBaseRequestHandler(BaseHTTPRequestHandler):
    def ret(self, text, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()
        self.wfile.write(text)

    def do_GET(self):
        res, type = self.get(self.path, {})
        self.ret(res, type)

    def do_POST(self):
        vars = self.parse_POST()
        log.debug(vars)
        res, type = self.post(self.path, vars)

        self.ret(res, type)

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                self.rfile.read(length),
                keep_blank_values=1)
        else:
            postvars = {}
        return postvars


class DummyHandler(MBaseRequestHandler):

    def post(self, url, vars):
        if url == "/update":
            return self.update(url, vars)
        elif url == "/insert":
            self.insert(vars)
            return self.index()

        data = db.searchurlpattern(self.path, "POST")

        if data is None:
            return "Doesn't exists!", "text/html"

        return data['data'], "application/json"

    def get(self, url, vars):
        if url == "/":
            return self.index()
        data = db.searchurlpattern(self.path, "GET")

        if data is None:
            return "Doesn't exists!", "text/html"

        return data['data'], "application/json"

    def insert(self, vars):
        log.debug(vars)
        url = vars['url'][0]
        method = vars['method'][0]
        type = vars['type'][0]
        data = vars['data'][0]
        db.insertroute(url, method, type, data)

    def index(self):
        log.debug("Index requested")

        apis = db.listpaths()

        return render_template("index.html", apis=apis), "text/html"

    def update(self, url, vars):
        log.debug(vars)
        db.update(
            vars['id'][0],
            vars['url'][0],
            vars['method'][0],
            vars['type'][0],
            vars['data'][0])
        return self.index()


def main():
    server = HTTPServer(('', port), DummyHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
