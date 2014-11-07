#!/bin/python
import os
def task_aptinstaller():
    return {
        'actions': ["bash aptinstalls"],
        'file_dep': ["aptinstalls"],
        'verbosity': 2
    }

def task_rundebugmode():
    return {
        "actions": ["python main.py dummytestdata.db 5000", ],
        "verbosity": 2
    }
