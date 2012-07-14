#!/usr/bin/env python

from datetime import datetime
import random
import time

from photon import Client, constants

client = Client(
    server="http://localhost:8000/",
    api_key="123456789",
)

while True:
    client.send(("random", random.randint(100, 999),), timestamp=datetime.now(), interval=constants.MINUTE)
    time.sleep(2)
