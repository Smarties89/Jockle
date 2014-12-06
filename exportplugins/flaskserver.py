#!/bin/python
# coding: utf-8


class FlaskServerExporter:
    name = "Flask Server"

    def __init__(self, appname):
        self._apis = []
        self._appname = appname

    def addapi(self, api):
        self._apis.append(api)

    def export(self):
        files = []

        files.append(self._makemain())
        files.append(self._makeblueprint())

        return files

    def _makeblueprint(self):
        blueprint = """#!/bin/python
# coding: utf-8
# Standard libraries
import logging

# Third party libraries
from flask import Blueprint

log = logging.getLogger()
app = Blueprint("blueprint", __name__)

"""
        for api in self._apis:
            blueprint += """
@app.route("{}", methods=["{}"])
def {}():
    return "{}", {}
""".format(
                api['url'],
                api['method'],
                api['url'].replace("/", "").replace("<", "").replace(">", ""),
                api['returndata'],
                api['returncode'])

        return {"data": blueprint, "filename": "blueprint.py"}

    def _makemain(self):
        main = """#!/bin/python
# coding: utf-8
# Standard libraries
import logging

# Third party libraries
from flask import Flask

# Project specific libraries
import blueprint

log = logging.getLogger()
app = Flask(__name__)

# TODO: Overwrite.
def debug():
    return True

if debug():
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
else:
    logging.basicConfig(filename="mylogs.txt")

app.register_blueprint(blueprint.app)


def main():
    app.debug = debug()
    if debug():
        log.info("Starting app in DEBUG mode")
        app.run(host="127.0.0.1", port=5000)
    else:
        log.info("Starting app in PRODUCTION mode")
        app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()"""
        return {"filename": "main.py", "data": main}
