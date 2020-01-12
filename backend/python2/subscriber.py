#!usr/bin/env/python

import paho.mqtt.client as mqtt


def on_connect(client, user_data, flags, rc):  # Method Execute when a client is connected to the server
    print("Connected to the MQTT Server")
    client.subscribe("merce")


def on_message_receive(client, user_data, msg):  # Method Executed when a  message is received
    if msg.payload == 'Q':
        client.disconnect()
    else:
        print(msg.payload)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message_receive

    client.loop_forever()
