#!/usr/bin/env python
import os
import sys
import importlib
import inspect
import pymongo

from django.conf import settings
from connection_to_mongodb import MongoBaseModel

def connect_to_mongodb(dict_class, app_name):
    for class_name, class_item in dict_class.items():
        if inspect.isclass(class_item) and issubclass(class_item, MongoBaseModel) and not class_item is MongoBaseModel:
            if hasattr(class_item, "fields"):
                collection = class_item().collection
                fields = class_item.fields
                for field, config in fields.items():
                    if isinstance(config, dict) and config.get("unique"):
                        collection.create_index([(field, pymongo.ASCENDING)], **config)
                    elif not isinstance(config, dict):
                        print(f"warning ==> config of field '{field}' in class '{class_name}' of app '{app_name}' is not a dictionary. Fix and migrate again to apply this config to mongodb. Every else config successfully apply to mongodb")
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
