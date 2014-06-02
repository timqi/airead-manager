__author__ = 'airead'

import os
import importlib

cur_path = os.path.dirname(os.path.realpath(__file__))

blueprints = {}

for dir_path, dir_name, filenames in os.walk(cur_path):
    print dir_path, dir_name, filenames
    subpath = dir_path.split('airead-manager' + os.path.sep)[1]
    modulePath = subpath.replace(os.path.sep, '.')
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        if ext == '.py' and name != '__init__':
            moduleName = modulePath + '.' + name
            print 'import', moduleName
            blueprints[name] = importlib.import_module(moduleName)