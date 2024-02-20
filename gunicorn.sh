#!/bin/sh
gunicorn run:app -w 2 --threads 2 -b 0.0.0.0:80 --access-logfile logs/access.log --error-logfile logs/message_validation.log --log-level info 