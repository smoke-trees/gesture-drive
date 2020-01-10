#!/usr/bin/env/python3

import paho.mqtt.client as mqtt
import signal
import time

if __name__ == "__main__":
    client = mqtt.Client()

    client.connect("localhost", 1883, 60)


    def shutdown(signal_num, frame):
        print("Shutting down publisher")
        client.disconnect()
        exit()


    signal.signal(signal.SIGINT, shutdown)

    while True:
        print("hello")
        time.sleep(3)
