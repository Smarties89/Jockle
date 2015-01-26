#!/bin/python
# coding: utf-8

from flask import render_template

class HTMLExporter:
    name = "HTML specification"

    def __init__(self, appname):
        self._apis = []
        self._appname = appname

    def addapi(self, api):
        self._apis.append(api)

    def export(self):

        return [
            {
                "filename": "index.html",
                "data": render_template("htmlexporter.html",  apis=self._apis)
            }
        ] 
