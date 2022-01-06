import asyncio
import websockets
import numpy as np
import datetime
import requests
import time
# from websocket import create_connection

# uri="ws://localhost:8765"
# uri = "ws://192.168.0.129:80"
# uri = "ws://192.168.50.65:80"
uri = "ws://192.168.10.53:8080"
# uri = "192.168.50.142:80"
# time1 = int(datetime.datetime.utcnow().timestamp())

def http_requests(ip='http://192.168.10.53:8080'):
    r = requests.get(ip)
    text_file = open("sample.txt", "w")
    n = text_file.write(r.text)
    text_file.close()
    data= np.loadtxt("./{}".format("sample.txt"),delimiter=',')
    return data

while True:
    print(http_requests())
    # time.sleep(3)