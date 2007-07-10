#!/bin/sh
cd $(dirname "$0")
export DJANGO_SETTINGS_MODULE=evolve.settings
export PYTHONPATH=$PATH:..
while true; do ./breeder.py; done
