#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import requests
from time import sleep
from datetime import datetime

class Watcher():
    def __init__(self, environ_lower):
        self.environ_lower = environ_lower
        self.vpn_state = 0
        self.data = {}
        self.headers = {"Content-Type": "application/json"}
        self.required_keywords = [
            "user",
            "token",
            "ip",
            "pushover"
        ]
        self.pushover_keywords = [
            "user",
            "token",
            "title",
            "priority",
            "url",
            "url_title",
            "device",
            "retry",
            "expire",
            "html",
            "attachment",
            "sound",
            "callback",
            "timestamp"
        ]
        self.verify_input()
        self.test_pushover()

    def timestamp(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def docker_log(self, text):
        os.system(f"echo {self.timestamp()} - {text} > /proc/1/fd/1")

    def send_pushover(self):
        response = requests.post(self.url, json.dumps(self.data), headers=self.headers)
        if response.status_code == 200:
            self.docker_log(f"Pushover: Message sent!")
        elif response.status_code == 400:
            self.docker_log(f"Pushover: {response.text}")
        elif response.status_code == 422:
            self.docker_log(f"Pushover: {response.text}")
        return response.text

    def verify_input(self):
        if not all(x in self.environ_lower for x in self.required_keywords):
            self.docker_log(f"Missing required invironment variable(s).")
        else:
            self.myip = self.environ_lower["ip"]
            self.url = self.environ_lower["pushover"]
            self.url = f"http://{self.url}" if "http" not in self.url else self.url
            self.url = f"{self.url}/push" if "push" not in self.url else self.url
            for keyword in self.pushover_keywords:
                if keyword in self.environ_lower:
                    self.data[keyword] = self.environ_lower[keyword]
            self.timer = int(self.environ_lower["timer"]) if "timer" in self.environ_lower else 360        

    def test_pushover(self):
        self.docker_log("Testing Pushover connection. You should recieve a message shortly.")
        self.data["message"] = "This message confirms Pushover is configured correctly."
        self.send_pushover()

    def watch(self):
        try:
            ip = requests.get("https://api.ipify.org").content.decode("utf8")
        except requests.exceptions.ConnectionError:
            if self.vpn_state == 0:
                self.data["message"] = "No connection through VPN Tunnel."
                self.docker_log(f"{self.data['message']}")
                self.send_pushover()
                self.vpn_state = 1
            elif self.vpn_state == 1:
                self.docker_log(f"{self.data['message']}")
        else:
            if self.myip == ip:
                self.data["message"] = "Your IP is being exposed / VPN Tunnel not working properly."
                if self.vpn_state == 0:
                    self.docker_log(f"{self.data['message']}")
                    self.send_pushover()
                    self.vpn_state = 1
                elif self.vpn_state == 1:
                    self.docker_log(f"{self.data['message']}")
            elif self.myip != ip:
                self.data["message"] = f"Everything seems to be normal, VPN IP: {ip}"
                if self.vpn_state == 1:
                    self.docker_log(f"{self.data['message']}")
                    self.send_pushover()
                    self.vpn_state = 0
                elif self.vpn_state == 0:
                    self.docker_log(f"{self.data['message']}")

if __name__ == "__main__":
    environ_lower = {key.lower(): os.environ[key] for key in os.environ}
    w = Watcher(environ_lower)
    while True:
        w.watch()
        sleep(w.timer)
