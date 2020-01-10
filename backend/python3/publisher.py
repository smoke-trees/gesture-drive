#!/usr/bin/env/python3

import paho.mqtt.client as mqtt
import signal
import time

if __name__ == "__main__":
    client = mqtt.Client()

    client.connect("localhost", 1883, 60)


    def shutdown(signal_num, frame):
        print("Shutting down publisher")
        client.publish("merce", "Q")
        client.disconnect()
        exit()


    signal.signal(signal.SIGINT, shutdown)

    while True:
        client.publish("merce", "hello")
        time.sleep(3)
