#!/usr/bin/env python

from datetime import datetime
import random
import time

from photon import Client

client = Client(
    server="http://localhost:8000/",
)

while True:
    # Push random data to a single line chart metric.
    client.send(
        samples=(("Indicator", random.randint(100, 999)),), 
        api_key='1', 
        timestamp=datetime.now(),
    )
    # Push random data to a multi-line chart metric.
    client.send(
        samples=(
            ("Line 1", random.randint(100, 999)),
            ("Line 2", random.randint(100, 999)),
            ("Line 3", random.randint(100, 999)),
            ("Line 4", random.randint(100, 999)),
            ("Line 5", random.randint(100, 999)),
        ), 
        api_key='2', 
        timestamp=datetime.now(),
    )
    # Push random data to a sample deviation metric.
    client.send(
        samples=(("Indicator", random.randint(100, 999)),), 
        api_key='3', 
        timestamp=datetime.now(),
    )
    # Push random data to a pie chart metric.
    client.send(
        samples=(
            ("Slice 1", random.randint(100, 999)),
            ("Slice 2", random.randint(100, 999)),
            ("Slice 3", random.randint(100, 999)),
            ("Slice 4", random.randint(100, 999)),
            ("Slice 5", random.randint(100, 999)),
        ), 
        api_key='4', 
        timestamp=datetime.now(),
    )
    time.sleep(2)
