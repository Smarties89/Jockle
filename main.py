#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv
from os import listdir
from os.path import join as joinpath
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


log = logging.getLogger()
dummypath = argv[1]
port = int(argv[2])

def debug():
    # TODO: implementer
    return True

if debug():
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
else:
    logging.basicConfig(filename="mylogs.txt")

def returnjsonfile(f):
    f = dummypath + "/" + f 
    log.debug("getting json file "+ f)

    with open(f) as fh:
        return fh.read(1024)

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()
        # Send the html message
        filename = self.path + ".get.json"

        result = returnjsonfile(filename)
        log.debug("trying to do {}".format(filename))
        self.wfile.write(result)
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()
        # Send the html message
        filename = joinpath(dummypath, self.path) + ".post.json"

        result = returnjsonfile(filename)
        log.debug("trying to do {}".format(filename))
        self.wfile.write(result)


def main():
    server = HTTPServer(('', port), DummyHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
