#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, make_response
from pushover import Pushover
import os

app = Flask(__name__)


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
        os.system(f"echo Missing input data: {content} > /proc/1/fd/1")
        return make_response("Missing either user, token or message in data.", 422)
    else:
        push = Pushover()
        result = push.message(**content)
        if result.answer["status"] == 1:
            os.system(f"echo Done: {result.answer} > /proc/1/fd/1")
            return make_response(f"{result.answer}", 200)
        else:
            os.system(f"echo Bad Request: {result.answer} > /proc/1/fd/1")
            return make_response(f"{result.answer}", 400)


app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
