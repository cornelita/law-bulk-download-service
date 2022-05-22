#!/bin/bash
python bd_service/protoc/generate_pb.py
python manage.py runserver 0.0.0.0:8000
