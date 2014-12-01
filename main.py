#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from jinja2 import Environment, FileSystemLoader
from cgi import parse_header, parse_multipart
from urlparse import parse_qs

from statuscodes import statuscodes
from mimes import mimes
from dbs import RouteDatabaseShelve 

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


db = RouteDatabaseShelve(dbpath)
#db.insertroute("/cards/[\w]*/categories", "POST", "json", '{"status": "hi"}')


class MBaseRequestHandler(BaseHTTPRequestHandler):
    def ret(self, text, type, returncode):
        self.send_response(returncode)
        self.send_header('Content-type', type)
        self.end_headers()
        self.wfile.write(text)

    def do_GET(self):
        res, type, returncode = self.get(self.path, {})
        self.ret(res, type, returncode)

    def do_POST(self):
        vars = self.parse_POST()
        log.debug(vars)
        res, type, returncode = self.post(self.path, vars)

        self.ret(res, type, returncode)

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
        if url == "/updatejockle":
            return self.update(url, vars)
        elif url == "/insertjockle":
            self.insert(vars)
            return self.index(), "text/html", 200

        data = db.searchurlpattern(self.path, "POST")

        if data is None:
            return "Doesn't exists!", "text/html", 200

        return data['returndata'], data['type'], data['returncode']

    def get(self, url, vars):
        if url == "/":
            return self.index()
        data = db.searchurlpattern(self.path, "GET")

        if data is None:
            return "Doesn't exists!", "text/html", 200

        return data['returndata'], data['type'], data['returncode']

    def insert(self, vars):
        log.debug(vars)
        url = vars['url'][0]
        method = vars['method'][0]
        type = vars['type'][0]
        returndata = vars['returndata'][0]
        returncode = int(vars['returncode'][0])
        db.insertroute(url, method, type, returndata, returncode)

    def index(self):
        log.debug("Index requested")

        apis = db.listpaths()
        return render_template("index.html", apis=apis, mimes=mimes, statuscodes=statuscodes), "text/html", 200

    def update(self, url, vars):
        log.debug(vars)
        db.update(
            vars['id'][0],
            vars['url'][0],
            vars['method'][0],
            vars['type'][0],
            int(vars['returndata'][0]),
            vars['returncode'][0])
        return self.index()


def main():
    server = HTTPServer(('', port), DummyHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
