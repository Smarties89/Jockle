#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv

from flask import render_template, Flask, request, redirect, jsonify
from fest.decorators import requireformdata

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


@app.errorhandler(404)
def not_found(error=None):

    message = {
        'status': 404,
        'message': 'Not Found: ' + request.path,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
    

def addapi(api):
    log.info("Adding '{}' as api".format(api['url']))
    app.add_url_rule(
        api['url'], # path
        api['url'], # name
        lambda: api['returndata'],
        methods=[api['method']])
        



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


@app.route("/")
def index():
    apis = db.listpaths()
    return render_template("index.html", apis=apis, mimes=mimes, statuscodes=statuscodes), 200


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
    app.run(host="0.0.0.0", port=port, extra_files=["dummytestdata.db"])


if __name__ == "__main__":
    main()
