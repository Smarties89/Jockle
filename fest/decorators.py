# Standard libraries
import logging
import sys
from functools import wraps
import traceback
from time import time
from uuid import uuid1

from flask import request

from fest.util import encode
from util import remote_addr


log = logging.getLogger("hest.decorators")


class RoleAuthenticator:
    def __init__(self, accessdeniedmsg, authenticate):
        self.accessdeniedmsg = accessdeniedmsg
        self.authenticate = authenticate

    def restrict(self, roles):
        def myactualdecorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):

                if self.authenticate(roles, args=args, kwargs=kwargs):
                    return f(*args, **kwargs)
                else:
                    return self.accessdeniedmsg

            return decorated
        return myactualdecorator


def validate(string, validator, errmsg): 
    def actualdecorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if validator(kwargs[string]):
                return f(*args, **kwargs)
            else:
                return errmsg, 500 

        return decorated

    return actualdecorator

def requireformdata(params):
    def myactualdecorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            for i in params:
                if not i in request.form:

                    log.debug("Invalid request, missing form data element {0}".format(i))

                    return "Invalid request, missing form data element {0}".format(i), 500
                kwargs[i] = request.form[i]
            result =  f(*args, **kwargs)
            return result

        return decorated
    return myactualdecorator

def addroutes(app, roleauthenticator):
    """ Adds useable routes to an Flask instance.
    
    Adds /ping[GET] and /shutdown[GET] to the Flask instance.
    Authentication is checked with the RoleAuthenticator
    instance roleauthenticator.
    """

    @app.route("/ping")
    @roleauthenticator.restrict(["admin"])
    def ping():
       return "up"

    @app.route("/shutdown")
    @roleauthenticator.restrict(["admin"])
    def shutdown():
        request.environ.get('werkzeug.server.shutdown')()

def wantedheaders():
    output = ""
    wanted = [
        "User-Agent",
        "Referer",
        "Accept",
        "Accept-Encoding",
        "Accept-Language"
    ]
         
    for i in wanted:
        if i in request.headers:
            output += "\n{}:{}".format(i, request.headers[i])

    return output.lstrip("\n")

def logapicall(result, t):
    log.info(
"""
==========================================================================
url: {0} [{1}] in {2}ms from srcip: {3}
{4}
==========================================================================
"""
.format(
    request.url,
    request.method,
    int(t*1000),
    remote_addr(), 
#    str(request.form).replace("ImmutableMultiDict(", "")[:-1],
    wantedheaders()
    ))


def logapicallexception(t, e):
    errnr = str(uuid1())
    log.error(
"""
==========================================================================
url: {} [{}] in {}ms from srcip: {} errnr: {}
{}
Exception: {}
traceback:
 - {}
==========================================================================
"""
.format(
    request.url,
    request.method,
    int(t*1000),
    remote_addr(), 
 #   str(request.form).replace("ImmutableMultiDict(", "")[:-1],
    errnr,
    wantedheaders(),
    e,
    traceback.format_exc().replace("\n", "\n - ")))
    return errnr

"""
   Decorator for API logging.
"""
def routelog(f): 
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        try:

            result = f(*args, **kwargs)
            end = time()
            logapicall(result, end-start)

            return result
        except Exception as e:
            errnr = logapicallexception(time()-start, e)

            return "Internal error, please contact support and ask them to look at log " + errnr, 500

    return wrapper


def _filenameoffunction(f):
    return sys.modules[f.__module__].__file__

class _CollectedLog:
    def __init__(self):
        self._sublogs = []
        self._resettimer()
    
    def _resettimer(self):
        self._timer = time()

    def _addlog(self, level, msg):
        self._sublogs.append(
            {
                "msg": msg,
                "level": level,
                "time": int(time()-self._timer) * 1000
            })
        self._resettimer()
        
    def critical(self, msg):
        self._addlog("CRITICAL", msg)
 
    def error(self, msg):
        self._addlog("ERROR", msg)
    
    def info(self, msg):
        self._addlog("INFO", msg)
    
    def warning(self, msg):
        self._addlog("WARNING", msg)
            
    def __dictit__(self):
        return self._sublogs


class CollectedLogger:
    def __init__(self, logger, exceptionhandler, remoteaddrfunction):
        self._logger = logger
        self._exceptionhandler = exceptionhandler
        self._remoteaddrfunction = remoteaddrfunction

    def _makedictlog(self, f, clog, t): 
        result = {
            "url": request.url,
            "method": request.method,
            "time": t,
            "src": self._remoteaddrfunction(),
            "filename": _filenameoffunction(f),
            "fname": f.__name__,
            "headers": wantedheaders(),
            "slogs": clog.__dictit__(),
        }
        return result

    def log(self, f): 
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time()
            clog = _CollectedLog()
            kwargs['log'] = clog
            try:
                result = f(*args, **kwargs)
                ld = self._makedictlog(
                    f,
                    clog,
                    int((time() - start)*1000))
                self._logger(ld)
                
                return result
            except Exception as e:
                ld = self._makedictlog(
                    f,
                    clog,
                    int((time() - start) * 1000))
                ld['stacktrace'] = traceback.format_exc()
                ld['exception'] =  e
                ld['errid'] = str(uuid1())
                self._exceptionhandler(ld)
                return "Internal error, please contact support and ask them to look at log {}".format(ld['errid']), 500
            
        return wrapper
