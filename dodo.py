#!/bin/python


def task_installdepedencies():
    return {
        'actions': ["bash installs"],
        'file_dep': ["installs"],
        'verbosity': 2
    }


def task_builddocker():
    return {
        "actions": ["sudo docker build -t jockle ."],
        "verbosity": 2
    }
