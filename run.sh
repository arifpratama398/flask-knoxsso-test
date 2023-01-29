#!/bin/bash

export FLASK_DEBUG=true
export FLASK_APP=app.py

flask run --host 0.0.0.0 --port 5005 --key key.pem --cert cert.pem
