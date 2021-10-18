#!/bin/bash

# install dependencies
/home/ubuntu/findTutorProject/DjangoEnv/bin/pip install -r /home/ubuntu/findTutorProject/findTutor/requirements.txt

# migrate
python3 /home/ubuntu/findTutorProject/findTutor/manage.py migrate