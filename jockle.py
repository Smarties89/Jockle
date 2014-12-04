#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv
from urlparse import urljoin

from flask import render_template, Flask, request, redirect, jsonify, Response
from fest.decorators import requireformdata
from flask import stream_with_context
import requests

from statuscodes import statuscodes
from mimes import mimes
from dbs import RouteDatabaseShelve 


log = logging.getLogger()
app = Flask(__name__)


def debug():
    # TODO: implementer
    return True


if debug():
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
else:
    logging.basicConfig()
    log.setLevel(logging.INFO)

def translateheaders(header):
    res = {}
    for r in header.keys():
        res[r] = header[r]


    return res

# This is handling the proxy functionality.
# Thanks to Zeray Rice for the stream proxy,
# see more here: http://flask.pocoo.org/snippets/118/
@app.errorhandler(404)
def not_found(error=None):
    url = urljoin(db.proxyurl(), request.path) 

    headers = translateheaders(request.headers)
    headers['Host'] = db.proxyurl().strip("http://")
    del headers["Content-Type"]
    del headers["Content-Length"]
    
    try:
        req = requests.request(
            request.method,
            url,
            data=request.data,
            headers=headers,
            stream=True)
    except Exception as e:
        return "404 or could not reach proxy server. Exception: {}".format(e), 404 

    log.info("Using proxy and serving '{}' with headers {}".format(url, headers))
    return Response(
            stream_with_context(req.iter_content()),
            content_type=req.headers['content-type'])
    

def addapi(api):
    log.info("Adding '{}' as api".format(api['url']))
    try:
        app.add_url_rule(
            api['url'], # path
            api['url'], # name
            lambda: Response(api['returndata'], mimetype=api['type']),
            methods=[api['method']])
    except Exception as e:
        log.warning("{} could not be added. Properly because it was a malformed url or already exists. Exception: {}".
            format(api['url'], e))


@app.route("/insertjockle", methods=["POST"])
@requireformdata(["url", "method", "type", "returndata", "returncode"])
def insertjockle(url, method, type, returndata, returncode):
    db.insertroute(url, method, type, returndata, returncode)
    return redirect("/")


@app.route("/updatejockle", methods=["POST"])
@requireformdata(["id", "url", "method", "type", "returndata", "returncode"])
def updatejockle(id, url, method, type, returndata, returncode):
    db.update(
        id,
        url,
        method,
        type,
        returndata,
        int(returncode))
    return redirect("/")


@app.route("/updatejockleproxy", methods=["POST"])
@requireformdata(["proxyurl"])
def updateproxy(proxyurl):
    db.setproxyurl(proxyurl)
    return redirect("/")


@app.route("/")
def index():
    apis = db.listpaths()
    return render_template("index.html", apis=apis, mimes=mimes, statuscodes=statuscodes, proxyurl=db.proxyurl()), 200


def main():
    try:
        dbpath = argv[1]
        port = int(argv[2])
    except:
        print("Wrong arguments. Please use python jockle.py <dbpath> <port>\n<dbpath> is the database file and <port> is the port to run the server on")
        return

    global db
    db = RouteDatabaseShelve(dbpath)

    for api in db.listpaths():
        addapi(api)
    app.debug = True
    app.run(host="0.0.0.0", port=port, extra_files=[dbpath])


if __name__ == "__main__":
    main()
