#!/bin/bash

#This script will update the git repository Remote-PI-Logging
#It will also ensur the .py files are exacuatble.

set -x

cd Remote-PI-Logging
git reset --hard HEAD
git pull
chmod +x *.py


