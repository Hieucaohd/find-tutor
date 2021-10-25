#!/usr/bin/env python
import os
import sys
import importlib
import inspect
import pymongo

from django.conf import settings
from connection_to_mongodb import MongoBaseModel

def connect_to_mongodb(dict_class, app_name):
    for class_name, mongo_class in dict_class.items():

        if inspect.isclass(mongo_class) and issubclass(mongo_class, MongoBaseModel) and not mongo_class is MongoBaseModel:
            print(f"Loading... ==> app {app_name}, class: {class_name}")
            
            if hasattr(mongo_class, "fields"):

                collection = mongo_class().collection
                
                fields = mongo_class.fields
                
                for field, config in fields.items():
                    
                    if isinstance(config, dict) and "unique" in config:
                        collection.create_index([(field, pymongo.ASCENDING)], unique=config["unique"])
                    
                    elif not isinstance(config, dict):
                        warning_message = f"""warning ==> config of field '{field}' in class '{class_name}' of app '{app_name}' is not a {dict}. 
                        Fix and migrate again to apply this config to mongodb. Every else config successfully apply to mongodb"""
                        print(warning_message)
            
            print(f"ok ==> app: {app_name}, class: {class_name}")


def migrate(list_apps):
    apps_not_found = []
    for app in list_apps:
        try:
            importlib.import_module(app)
        except ModuleNotFoundError:
            apps_not_found.append(app)

    if len(apps_not_found) != 0:
        for app in apps_not_found:
            print("not found app", app)
        print("not do anything yet.")
        return
    
    for app in list_apps:
        try:
            local_func = locals()
            exec(f"from {app} import mongoModels", globals(), local_func)
            mongoModels = local_func["mongoModels"]
            connect_to_mongodb(dict_class=mongoModels.__dict__, app_name=app)
        except ModuleNotFoundError:
            print("warning ==> not found mongoModels.py file in app", app)
        except ImportError:
            print("warning ==> not found mongoModels.py file in app", app)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findTeacherProject.settings')
    argv = sys.argv

    if len(argv) == 2:
        if argv[1] == "migrate":
            list_apps = settings.INSTALLED_APPS
            migrate(list_apps=list_apps)
    elif len(argv) > 2:
        if argv[1] == "migrate":
            list_apps = argv[2:]
            migrate(list_apps=list_apps)

if __name__ == "__main__":
    main()
