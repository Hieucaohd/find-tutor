#!/bin/bash

/home/ubuntu/findTutorProject/DjangoEnv/bin/source /home/ubuntu/findTutorProject/findTutor/.env

# install dependencies
/home/ubuntu/findTutorProject/DjangoEnv/bin/pip install -r /home/ubuntu/findTutorProject/findTutor/requirements.txt

# migrate
/home/ubuntu/findTutorProject/DjangoEnv/bin/python3 /home/ubuntu/findTutorProject/findTutor/manage.py migrate