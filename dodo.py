#!/bin/python
import os
def task_installdepedencies():
    return {
        'actions': ["bash installs"],
        'file_dep': ["installs"],
        'verbosity': 2
    }

def task_rundebug():
    return {
        "actions": ["python jockle.py dummytestdata.db 5000", ],
        "verbosity": 2
    }
