#!/bin/bash

/home/ubuntu/findTutorProject/DjangoEnv/bin/pip install -r /home/ubuntu/findTutorProject/findTutor/requirements.txt

# stop the supervisor running django app
supervisorctl start findTutorDjango