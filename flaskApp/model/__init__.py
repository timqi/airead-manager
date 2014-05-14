import os
import importlib

cur_path = os.path.dirname(os.path.realpath(__file__))

modules = {}

for dir_path, dir_name, filenames in os.walk(cur_path):
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        if ext == '.py':
            moduleName = 'model.' + name
            modules[name] = importlib.import_module(moduleName)


db = modules['db_declare'].db
