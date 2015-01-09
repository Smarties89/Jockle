#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv
from urlparse import urljoin
from zipfile import ZipFile

from flask import render_template, Flask, request, redirect, Response
from fest.decorators import requireformdata
import requests

from statuscodes import statuscodes
from mimes import mimes
from dbs import RouteDatabaseShelve
import exportplugins

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
        res[r] = header[r].encode("ASCII")

    return res


# This is handling the proxy functionality.
# Thanks to Zeray Rice for the stream proxy,
# see more here: http://flask.pocoo.org/snippets/118/
@app.errorhandler(404)
def not_found(error=None):
    url = urljoin(db.proxyurl(), request.path).encode("ASCII")

    headers = translateheaders(request.headers)
    headers['Host'] = db.proxyurl().lstrip("http://").lstrip("https://").rstrip("/").encode("ASCII")

    del headers["Content-Type"]
    del headers["Content-Length"]

    try:
        log.info("Requesting {} [{}] data: '{}'".format(url, request.method, request.data))
        print("headers")
        for h in headers:
            print(" - '{}':'{}'".format(h, headers[h]))

        req = requests.request(
            request.method,
            url,
            data=request.data,
            allow_redirects=False,
            headers=headers)

        return req.content
    except Exception as e:
        return "404 or could not reach proxy server. Exception: {}".format(e), 404 
 

def addapi(api):
    log.info("Adding '{}' as api".format(api['url']))
    try:
        app.add_url_rule(
            api['url'],  # path
            api['url'],  # name
            lambda: Response(api['returndata'], mimetype=api['type']),
            methods=[api['method']])
    except Exception as e:
        log.warning("{} could not be added. Properly because it was a malformed url or already exists. Exception: {}".
            format(api['url'], e))


@app.route("/insertjockle", methods=["POST"])
@requireformdata(["url", "method", "type", "returndata", "returncode"])
def insertjockle(url, method, type, returndata, returncode):
    db.insertroute(url, method, type, returndata, returncode)
    return redirect("/jockle")


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
    return redirect("/jockle")


@app.route("/updatejockleproxy", methods=["POST"])
@requireformdata(["proxyurl"])
def updateproxy(proxyurl):
    db.setproxyurl(proxyurl)
    return redirect("/jockle")


@app.route("/exportjockle")
def useexportplugin():
    pluginnr = int(request.args['pluginnr'])
    e = exportplugins.plugins[pluginnr]("some name")
    for api in db.listpaths():
        e.addapi(api)
    z = ZipFile("static/exported.zip", "w")
    for f in e.export():
        # Makes a new file called name.
        z.writestr(f['filename'], f['data'])
    z.close()
    return app.send_static_file("exported.zip")



@app.route("/jockle")
def index():
    apis = db.listpaths()
    return render_template(
        "index.html",
        apis=apis,
        mimes=mimes,
        statuscodes=statuscodes,
        proxyurl=db.proxyurl(),
        exportplugins=exportplugins.plugins
        ), 200


def main():
    global dbpath
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
