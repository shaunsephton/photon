#!/usr/bin/env python

from datetime import datetime
import random
import time

from photon import Client, constants

client = Client(
    server="http://localhost:8000/",
    project="sample",
    api_key="12345",
)

while True:
    client.send(("random", random.randint(100, 999),), metric_slug='randomizer', timestamp=datetime.now(), interval=constants.MINUTE)
    time.sleep(60)
