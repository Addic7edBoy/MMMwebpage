#!/bin/bash
# flask db init
# flask db upgrade
gunicorn --bind 0.0.0.0:5000 microblog:app
