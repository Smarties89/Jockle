#!/bin/python
# coding: utf-8
# Standard libraries
import logging
from sys import argv
from urlparse import urljoin
from zipfile import ZipFile

from flask import render_template, Flask, request, redirect, Response, make_response
from fest.decorators import requireformdata
import requests

from statuscodes import statuscodes
from mimes import mimes
from dbs import RouteDatabaseShelve
import exportplugins

log = logging.getLogger("jockle")
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


#################################################
###########  API for controlling jockle. ########
#################################################


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


@app.route("/jockledelete")
def jockledelete():
    url = request.args.get("url")
    log.info("Deleting {}".format(url))
    db.delete(url)
    return redirect("/jockle")


################################################
########### API for proxying calls. ############
################################################

def translateheaders(header):
    res = {}
    for r in header.keys():
        res[r] = header[r]  # .encode("ASCII")

    return res


def create_response(exres):
    resp = make_response(exres.content)

    log.debug("create_response: Adding headers to response from exres")
    for i in exres.headers:
        # It might be chunked, and we send it back in one piece.
        if i.lower() == "transfer-encoding":
            log.debug("create_response: \tNot added transfer-encoding: '{}' from resp header".
                format(exres.headers[i]))
            continue
        
        # This is appended on afterwards. Python-Flask requires it to
        #  be added as 'resp.mimetype = xxx' instead of as a header
        if i.lower() == "content-type":
            log.debug("create_response: \tNot added content-type: '{}' from resp header".
                format(exres.headers[i]))
            continue
    
        # TODO: Set referer


        # This is because we might get gzip, but python-request will
        # automatically unzip it and what we respond to the client
        # will not be zipped.
        if i.lower() == "content-encoding":
            log.debug("create_response: \tNot added content-encoding.")
            continue
       
       # We get a cookie
#        if i.lower() == "cookie":
#            resp.headers['Set-Cookies'] = exres.headers[i]
#            continue

        resp.headers[i] = exres.headers[i]
        log.debug("create_response: \t- '{}' = '{}'".format(i, exres.headers[i]))

    log.debug("create_response: Setting status_code to {}".format(exres.status_code))
    resp.status_code = exres.status_code

    # Setting the mimetype. Python flask sets the charset automatically
    if 'content-type' in  exres.headers:
        log.debug("create_response: Setting mimetype to {}".
                format(exres.headers['content-type'].split(";")[0]))
        resp.mimetype = exres.headers['content-type'].split(";")[0]
    
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def gethostforproxy():
    """
        Takes the proxy url and strips it so it will work as header
        in the reuqest to the external service.
    """
    host = db.proxyurl()
    if host.startswith("https://"):
        host = host.lstrip("https://")
    elif host.startswith("http://"):
        host = host.lstrip("http://")

    if host.endswith("/"):
        host = host.rstrip("/")

    return host

def externalcall(url):
    """
        This does the actual proxy call and returns the response
    """
    
    headers = translateheaders(request.headers)
    headers['Host'] = gethostforproxy()

    log.debug("externalcall: Original host: '{}' now host:'{}'".format(db.proxyurl(), headers['Host']))
    # TODO: look at http://docs.python-requests.org/en/latest/api/#requests.Response to see what to transfer.

    # Why have this ever been here?
    del headers["Content-Type"]

    # TODO: Set referer
    #  Referer: http://127.0.0.1:5006/translator/translate.html
    #  Referer: http://sunday.zone/translator/translate.html


    # This will python requset automatically add.
    del headers["Content-Length"]

    log.debug("externalcall: headers for ")
    for h in headers:
        log.debug("externalcall: \t- '{}':'{}'".format(h, headers[h]))

    log.info("externalcall: requesting {} [{}] data: '{}'".format(url, request.method, request.data))
    exres = requests.request(
        request.method,
        url,
        data=request.environ['body_copy'], 
        allow_redirects=False,
        headers=headers)

    return exres


# This is handling the proxy functionality.
@app.errorhandler(404)
def not_found(error=None):
    try:
        url = urljoin(db.proxyurl(), request.path) # .encode("ASCII")
        log.info("Preparing proxy call to {}".format(url))
        exres = externalcall(url)

        log.debug("Creating the response")
        resp = create_response(exres)

        log.debug("Response created. Now returning it")
        return resp # exres.content # resp
    except Exception as e:
        return "404 or could not reach proxy server. Exception: {}".format(e), 404 


# Thanks to jhasi at stackoverflow
# http://stackoverflow.com/questions/10999990/get-raw-post-body-in-python-flask-regardless-of-content-type-header
class WSGICopyBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        from cStringIO import StringIO
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['body_copy'] = body
        environ['wsgi.input'] = StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, 
                                    self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback

app.wsgi_app = WSGICopyBody(app.wsgi_app)



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
