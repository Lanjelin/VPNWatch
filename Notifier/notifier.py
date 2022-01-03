#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pushover import Pushover
from datetime import datetime
from gevent.pywsgi import WSGIServer
from flask import Flask, request, make_response

app = Flask(__name__)

def timestamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def docker_log(text):
    os.system(f"echo {timestamp()} - {text} > /proc/1/fd/1")

@app.route("/", methods=["GET", "POST"])
def index():
    return make_response(
        "POST a request to /push with at least token, user and message as data.",
        200,
        None,
    )


@app.route("/push", methods=["POST"])
def push():
    content = request.get_json()
    if not all(x in content for x in ["user", "token", "message"]):
        docker_log(f"Missing input data: {content}")
        return make_response("Missing either user, token or message in data.", 422)
    else:
        push = Pushover()
        result = push.message(**content)
        if result.answer["status"] == 1:
            docker_log(f"Message sent: {result.answer}")
            return make_response(f"{result.answer}", 200)
        else:
            docker_log(f"Bad Request: {result.answer}")
            return make_response(f"{result.answer}", 400)

if __name__ == "__main__":
    docker_log(f"Running Pushover Notifier.")
    docker_log(f"POST a request to /push with at least token, user and message as data.")
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
