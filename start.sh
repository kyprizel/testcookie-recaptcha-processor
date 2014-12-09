#!/bin/sh

gunicorn -c gunicorn.conf.py app:app
