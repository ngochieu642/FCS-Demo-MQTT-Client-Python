import os
import time
import uuid

import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print('Connected with result code: ' + str(rc))

    client.subscribe(socket_topic_id)
    print('Subscribed')

    ret, mid = client.publish(socket_topic_id, payload=json.dumps(transfer_msg), qos=0, retain=False, properties=None)
    print(f'Return message: {ret}')


def on_message(client, userdata, msg):
    print(f'client: {client}')
    print(f'userdata: {userdata}')
    print(f'msg: {msg}')


def on_disconnect(client, userdata, msg):
    print(client, userdata, msg)


if __name__ == "__main__":
    # Create buffer
    socket_topic_id = socket_client_id = str(uuid.uuid4())
    msg_id = str(uuid.uuid4())

    hello_msg = {"message_id": msg_id, "topic": socket_topic_id, "client_id": socket_client_id}
    transfer_msg = {
        "message_type": 1001,
        # "message_name": "This message could be custom",
        "message_content": json.dumps(hello_msg),
        "STX": 9001,
        "ETX": 9002
    }

    transfer_msg_buffer = bytearray(json.dumps(transfer_msg), 'utf-8')

    # Init Client
    client = mqtt.Client(transport="websockets")
    client.ws_set_options(path="/mqtt", headers=None)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        SERVER_HOST = '172.16.2.127'
        SERVER_PORT = 1889
        client.connect(host=SERVER_HOST, port=int(SERVER_PORT), keepalive=60)

    except Exception as e:
        print(e)

    client.loop_forever()
